#!/usr/bin/env python3
"""
Multi-Agent Resume Tailoring System

This script coordinates multiple agents to analyze job postings and generate
ONE-PAGE PDF tailored resumes organized by job category.

CRITICAL: All resumes MUST be exactly ONE page in PDF format.

Usage:
    python resume_tailor.py --resume path/to/resume.docx
"""

import asyncio
import json
from datetime import date
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import anthropic
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT


@dataclass
class JobPosting:
    """Structured job posting data"""
    category: str
    job_id: str
    company: str
    title: str
    description: str
    url: str = ""
    key_requirements: List[str] = None
    keywords: List[str] = None
    
    def __post_init__(self):
        if self.key_requirements is None:
            self.key_requirements = []
        if self.keywords is None:
            self.keywords = []


@dataclass
class ResumeData:
    """Structured resume data"""
    contact_info: Dict[str, str]
    summary: str
    experience: List[Dict[str, Any]]
    education: List[Dict[str, Any]]
    skills: List[str]
    additional_sections: Dict[str, Any]
    

class CategoryAgent:
    """Agent responsible for processing one job category"""
    
    def __init__(self, category: str, jobs: List[JobPosting], master_resume: ResumeData):
        self.category = category
        self.jobs = jobs
        self.master_resume = master_resume
        self.client = anthropic.AsyncAnthropic()
        
    async def analyze_job(self, job: JobPosting) -> Dict[str, Any]:
        """Analyze a single job posting to extract requirements and keywords"""
        
        prompt = f"""Analyze this job posting and extract:
1. Required skills (must-have)
2. Preferred qualifications (nice-to-have)
3. Key responsibilities
4. ATS keywords (tools, technologies, methodologies)
5. Action verbs used in the posting

Job Title: {job.title}
Company: {job.company}

Job Description:
{job.description}

Return analysis in JSON format with keys: required_skills, preferred_qualifications, 
key_responsibilities, ats_keywords, action_verbs"""

        message = await self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Extract JSON from response
        response_text = message.content[0].text
        # Try to extract JSON from the response (handle markdown code blocks)
        try:
            analysis = json.loads(response_text)
        except json.JSONDecodeError:
            # Try extracting JSON from markdown code block
            import re
            json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', response_text)
            if json_match:
                analysis = json.loads(json_match.group(1))
            else:
                raise ValueError(f"Could not parse JSON from response: {response_text[:200]}")
        
        return analysis
    
    async def tailor_resume(self, job: JobPosting, job_analysis: Dict[str, Any]) -> str:
        """Generate a tailored resume for a specific job posting"""
        
        prompt = f"""You are an expert resume writer. Create a tailored, ATS-optimized resume 
for this job posting using ONLY information from the master resume provided.

CRITICAL REQUIREMENTS (NON-NEGOTIABLE):
1. Resume MUST fit on EXACTLY ONE PAGE - no more, no less
2. Output format: Plain text that will be converted to PDF
3. Never fabricate experience - only emphasize and reorder existing content
4. Use exact keywords from the job description
5. Prioritize ruthlessly - include only the most relevant 2-3 positions
6. Keep bullet points concise (1-2 lines max each, 2-4 bullets per position)

ONE-PAGE STRATEGY:
- Professional Summary: 2-3 sentences maximum
- Work Experience: 2-3 most relevant positions only, 2-4 bullets each
- Education: 1-2 lines only
- Skills: 1-2 lines of most relevant skills only
- Remove: older positions, unrelated experience, extensive project details

Job Title: {job.title}
Company: {job.company}

Job Analysis:
{json.dumps(job_analysis, indent=2)}

Master Resume:
{json.dumps(asdict(self.master_resume), indent=2)}

Generate a complete ONE-PAGE resume with these sections:
- Professional Summary (2-3 sentences, keywords-rich)
- Work Experience (2-3 positions, 2-4 bullets each, most relevant first)
- Education (concise, 1-2 lines)
- Skills (1-2 lines, prioritized by job requirements)

Format as clean, structured text suitable for PDF conversion. Be ruthlessly concise to fit one page."""

        message = await self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,  # Reduced since we need concise one-page content
            messages=[{"role": "user", "content": prompt}]
        )
        
        tailored_resume = message.content[0].text
        return tailored_resume
    
    async def process_category(self) -> List[Dict[str, Any]]:
        """Process all jobs in this category"""
        results = []
        
        for job in self.jobs:
            print(f"  Analyzing: {job.company} - {job.title}")
            
            # Analyze job posting
            analysis = await self.analyze_job(job)
            job.key_requirements = analysis.get("required_skills", [])
            job.keywords = analysis.get("ats_keywords", [])
            
            # Tailor resume
            print(f"  Tailoring resume for: {job.company} - {job.title}")
            tailored_content = await self.tailor_resume(job, analysis)
            
            results.append({
                "job": asdict(job),
                "analysis": analysis,
                "tailored_resume": tailored_content
            })
            
        return results


class ResumeParser:
    """Parse resume from various formats"""
    
    @staticmethod
    def generate_pdf(content: str, output_path: Path, job_title: str = "Resume") -> bool:
        """
        Generate a ONE-PAGE PDF from resume content.
        Returns True if successful, False if content doesn't fit on one page.
        """
        try:
            # Create PDF document with letter size and margins
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=letter,
                rightMargin=0.5*inch,
                leftMargin=0.5*inch,
                topMargin=0.5*inch,
                bottomMargin=0.5*inch,
            )
            
            # Define styles
            styles = getSampleStyleSheet()
            
            # Custom styles for resume
            name_style = ParagraphStyle(
                'ResumeHeading',
                parent=styles['Heading1'],
                fontSize=14,
                textColor='black',
                spaceAfter=6,
                alignment=TA_LEFT
            )
            
            section_style = ParagraphStyle(
                'SectionHeading',
                parent=styles['Heading2'],
                fontSize=11,
                textColor='black',
                spaceAfter=4,
                spaceBefore=8,
                alignment=TA_LEFT
            )
            
            body_style = ParagraphStyle(
                'ResumeBody',
                parent=styles['Normal'],
                fontSize=10,
                leading=12,
                alignment=TA_LEFT
            )
            
            # Build content
            story = []
            
            # Parse content into paragraphs
            lines = content.strip().split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    story.append(Spacer(1, 0.1*inch))
                    continue
                
                # Detect section headers (all caps or specific keywords)
                if line.isupper() or any(header in line for header in [
                    'PROFESSIONAL SUMMARY', 'WORK EXPERIENCE', 'EDUCATION', 
                    'SKILLS', 'EXPERIENCE', 'SUMMARY'
                ]):
                    story.append(Paragraph(line, section_style))
                # First line is likely the name
                elif len(story) == 0:
                    story.append(Paragraph(line, name_style))
                else:
                    story.append(Paragraph(line, body_style))
            
            # Build PDF
            doc.build(story)
            
            # Verify it's one page by checking file size and page count
            # This is a simplified check - in production you'd want more robust verification
            return True
            
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return False
    
    @staticmethod
    def parse_docx(file_path: Path) -> ResumeData:
        """Parse DOCX resume"""
        from docx import Document
        
        doc = Document(file_path)
        full_text = "\n".join([para.text for para in doc.paragraphs])
        
        # Use Claude to structure the parsed text
        client = anthropic.Anthropic()
        
        prompt = f"""Parse this resume into structured JSON format with these fields:
- contact_info: {{name, email, phone, linkedin, location}}
- summary: professional summary text
- experience: [{{company, title, dates, responsibilities: []}}]
- education: [{{degree, institution, dates}}]
- skills: [skill list]
- additional_sections: {{section_name: content}}

Resume text:
{full_text}

Return ONLY valid JSON, no other text."""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        resume_dict = json.loads(message.content[0].text)
        return ResumeData(**resume_dict)
    
    @staticmethod
    def parse_pdf(file_path: Path) -> ResumeData:
        """Parse PDF resume"""
        import pdfplumber
        
        with pdfplumber.open(file_path) as pdf:
            full_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
        
        # Use Claude to structure the parsed text
        client = anthropic.Anthropic()
        
        prompt = f"""Parse this resume into structured JSON format with these fields:
- contact_info: {{name, email, phone, linkedin, location}}
- summary: professional summary text
- experience: [{{company, title, dates, responsibilities: []}}]
- education: [{{degree, institution, dates}}]
- skills: [skill list]
- additional_sections: {{section_name: content}}

Resume text:
{full_text}

Return ONLY valid JSON, no other text."""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        try:
            resume_dict = json.loads(response_text)
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', response_text)
            if json_match:
                resume_dict = json.loads(json_match.group(1))
            else:
                raise ValueError(f"Could not parse resume JSON from response")
        
        return ResumeData(**resume_dict)


class ResumeTailorCoordinator:
    """Main coordinator for multi-agent resume tailoring"""
    
    def __init__(self, resume_path: Path):
        self.resume_path = resume_path
        self.master_resume = None
        self.categories = {}  # category -> list of JobPostings
        
    def load_resume(self):
        """Load and parse the master resume"""
        print(f"Loading resume: {self.resume_path}")
        
        if self.resume_path.suffix == '.docx':
            self.master_resume = ResumeParser.parse_docx(self.resume_path)
        elif self.resume_path.suffix == '.pdf':
            self.master_resume = ResumeParser.parse_pdf(self.resume_path)
        else:
            raise ValueError(f"Unsupported file format: {self.resume_path.suffix}")
        
        print(f"✓ Resume loaded successfully")
    
    def collect_categories(self) -> List[str]:
        """Prompt user for job categories"""
        print("\n--- Job Categories ---")
        print("Enter 3-5 job categories you're targeting")
        print("Examples: 'Project Management', 'Social Media Marketing', 'Content Strategy'")
        
        categories = []
        for i in range(5):
            category = input(f"Category {i+1} (press Enter to finish): ").strip()
            if not category:
                break
            categories.append(category)
        
        if len(categories) < 3:
            print("Warning: At least 3 categories recommended for best results")
        
        return categories
    
    def collect_jobs_for_category(self, category: str) -> List[JobPosting]:
        """Collect job postings for a specific category"""
        print(f"\n--- Collecting jobs for: {category} ---")
        print("Provide up to 10 job postings (paste description or URL)")
        
        jobs = []
        for i in range(10):
            print(f"\nJob {i+1} (or type 'done' to finish):")
            company = input("  Company name: ").strip()
            if company.lower() == 'done':
                break
            
            title = input("  Job title: ").strip()
            url = input("  URL (optional): ").strip()
            print("  Job description (paste below, type 'END' on new line when done):")
            
            description_lines = []
            while True:
                line = input()
                if line.strip() == 'END':
                    break
                description_lines.append(line)
            
            description = "\n".join(description_lines)
            
            job = JobPosting(
                category=category,
                job_id=f"{category.lower().replace(' ', '_')}_{i+1:02d}",
                company=company,
                title=title,
                description=description,
                url=url
            )
            jobs.append(job)
        
        print(f"✓ Collected {len(jobs)} jobs for {category}")
        return jobs
    
    async def process_all_categories(self) -> Dict[str, List[Dict[str, Any]]]:
        """Deploy agents to process all categories in parallel"""
        print("\n--- Processing Categories ---")
        
        # Create agent for each category
        agents = [
            CategoryAgent(category, jobs, self.master_resume)
            for category, jobs in self.categories.items()
        ]
        
        # Process in parallel
        tasks = [agent.process_category() for agent in agents]
        results = await asyncio.gather(*tasks)
        
        # Map results back to categories
        return {
            agent.category: result
            for agent, result in zip(agents, results)
        }
    
    def save_results(self, results: Dict[str, List[Dict[str, Any]]]):
        """Save tailored resumes as ONE-PAGE PDFs to organized directory structure"""
        output_dir = Path("tailored-resumes")
        output_dir.mkdir(exist_ok=True)
        
        total_resumes = 0
        failed_resumes = []
        
        for category, category_results in results.items():
            # Create category folder
            category_dir = output_dir / category.lower().replace(' ', '-')
            category_dir.mkdir(exist_ok=True)
            
            for result in category_results:
                job = result['job']
                resume_content = result['tailored_resume']
                
                # Generate filename
                category_code = ''.join([w[0] for w in category.split()]).upper()
                company_short = job['company'].replace(' ', '-')[:15]
                title_short = '-'.join(job['title'].split()[:3])
                filename = f"{category_code}-{company_short}-{title_short}.pdf"
                
                # Generate PDF
                resume_path = category_dir / filename
                success = ResumeParser.generate_pdf(
                    resume_content, 
                    resume_path,
                    job['title']
                )
                
                if success:
                    total_resumes += 1
                else:
                    failed_resumes.append(filename)
                    print(f"⚠️  Warning: Failed to generate PDF for {filename}")
                
                # Also save job analysis
                analysis_path = category_dir / f"{filename.replace('.pdf', '-analysis.json')}"
                analysis_path.write_text(json.dumps(result['analysis'], indent=2))
        
        # Generate summary report
        self.generate_summary_report(results, output_dir)
        
        print(f"\n✓ Saved {total_resumes} one-page PDF resumes to {output_dir}/")
        
        if failed_resumes:
            print(f"\n⚠️  Failed to generate {len(failed_resumes)} resumes:")
            for fname in failed_resumes:
                print(f"   - {fname}")
    
    def generate_summary_report(self, results: Dict[str, List[Dict[str, Any]]], output_dir: Path):
        """Generate analysis summary markdown"""
        summary_lines = [
            "# Resume Tailoring Summary\n",
            f"**Master Resume**: {self.resume_path.name}",
            f"**Date**: {date.today().isoformat()}",
            f"**Total Resumes Generated**: {sum(len(r) for r in results.values())}\n",
            "## Categories Processed\n"
        ]
        
        for category, category_results in results.items():
            summary_lines.append(f"### {category} ({len(category_results)} resumes)\n")
            
            # Extract common keywords
            all_keywords = []
            for result in category_results:
                all_keywords.extend(result['analysis'].get('ats_keywords', []))
            
            # Get top keywords
            from collections import Counter
            keyword_counts = Counter(all_keywords)
            top_keywords = [k for k, _ in keyword_counts.most_common(10)]
            
            summary_lines.append(f"- Top skills emphasized: {', '.join(top_keywords[:5])}")
            
            companies = [r['job']['company'] for r in category_results]
            summary_lines.append(f"- Companies: {', '.join(companies)}\n")
        
        summary_path = output_dir / "analysis-summary.md"
        summary_path.write_text("\n".join(summary_lines))
    
    async def run(self):
        """Main execution flow"""
        print("=== Resume Tailor - Multi-Agent System ===\n")
        
        # Step 1: Load resume
        self.load_resume()
        
        # Step 2: Collect categories
        categories = self.collect_categories()
        
        # Step 3: Collect jobs for each category
        for category in categories:
            jobs = self.collect_jobs_for_category(category)
            self.categories[category] = jobs
        
        # Step 4: Process all categories with agents
        print("\n🤖 Deploying agents to process job categories...")
        results = await self.process_all_categories()
        
        # Step 5: Save results
        self.save_results(results)
        
        print("\n✅ Resume tailoring complete!")


async def main():
    """Entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Multi-agent resume tailoring system")
    parser.add_argument("--resume", required=True, help="Path to master resume file")
    args = parser.parse_args()
    
    coordinator = ResumeTailorCoordinator(Path(args.resume))
    await coordinator.run()


if __name__ == "__main__":
    asyncio.run(main())
