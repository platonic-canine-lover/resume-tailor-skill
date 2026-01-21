---
name: resume-tailor
description: Multi-agent resume tailoring system for job applications. Use when users want to create customized resumes for multiple job categories and postings. Triggered by requests to "tailor my resume," "create custom resumes for jobs," "optimize resume for multiple positions," or when users upload a resume and mention creating versions for different job types. This skill coordinates multiple agents to analyze job postings and generate ATS-optimized, tailored resumes organized by job category.
---

# Resume Tailor - Multi-Agent Job Application System

This skill enables Claude Code to parse a user's master resume and generate tailored, ATS-optimized versions for up to 50 job postings across 3-5 categories using parallel agent coordination.

## CRITICAL REQUIREMENTS

**ALL GENERATED RESUMES MUST BE:**
- ✅ **EXACTLY ONE PAGE** - No more, no less
- ✅ **PDF FORMAT ONLY** - Never DOCX or other formats

These are non-negotiable constraints that must be enforced in every output.

## Installation Requirements

Before using this skill, ensure these dependencies are installed:

```bash
pip install anthropic pdfplumber reportlab --break-system-packages
```

Or use the included requirements.txt:

```bash
pip install -r requirements.txt --break-system-packages
```

The `resume_tailor.py` script can be run directly or integrated into Claude Code workflows.

## Workflow Overview

1. **Resume Intake**: Parse user's master resume
2. **Category Definition**: Collect 3-5 job categories from user
3. **Job Collection**: Gather up to 10 job postings per category
4. **Multi-Agent Analysis**: Deploy parallel agents to analyze jobs and tailor resumes
5. **Output Organization**: Store results in category-named folders

## Step 1: Resume Parsing

### Supported Input Formats
- `.docx` (preferred for parsing)
- `.pdf` (requires text extraction)
- `.txt` or `.md` (plain text)

**Note**: Input can be any format, but ALL output resumes will be PDF only.

### Parsing Strategy

```python
# For DOCX files
from docx import Document
doc = Document(resume_path)
full_text = "\n".join([para.text for para in doc.paragraphs])

# For PDF files
import pdfplumber
with pdfplumber.open(resume_path) as pdf:
    full_text = "\n".join([page.extract_text() for page in pdf.pages])
```

### Extract and Structure Resume Data

Parse the resume into structured components:
- **Contact Information**: Name, email, phone, LinkedIn, location
- **Professional Summary**: Opening statement/objective
- **Work Experience**: Company, title, dates, responsibilities, achievements
- **Education**: Degrees, institutions, dates, relevant coursework
- **Skills**: Technical skills, soft skills, tools, certifications
- **Additional Sections**: Projects, publications, volunteering, languages

Store as structured dictionary or JSON for easy manipulation.

## Step 2: Category Collection

Prompt user for 3-5 job categories. Examples:
- "Project Management"
- "Social Media Marketing"
- "Technical Writing"
- "Product Marketing"
- "Content Strategy"

Validate categories are specific enough to differentiate job requirements but broad enough to group similar roles.

## Step 3: Job Posting Collection

For each category, collect up to 10 job postings:

### Collection Methods
1. **User pastes job description text**
2. **User provides job posting URLs** (fetch with web_fetch if accessible)
3. **User uploads job descriptions as files**

### Job Data Structure

Store each job posting with:
```python
{
    "category": "Social Media Marketing",
    "job_id": "smm_01",
    "company": "Company Name",
    "title": "Social Media Manager",
    "description": "Full job description text...",
    "url": "https://...",
    "key_requirements": [],  # Extracted during analysis
    "keywords": []           # Extracted during analysis
}
```

## Step 4: Multi-Agent Analysis Architecture

Deploy one agent per job category for parallel processing. Each agent:
1. Analyzes all job postings in its category
2. Identifies common requirements and keywords
3. Maps user's resume to each job posting
4. Generates tailored resume for each posting

### Agent Coordination Pattern

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def process_category(category_name, jobs, master_resume):
    """Each agent processes one category"""
    tailored_resumes = []
    
    for job in jobs:
        # Analyze job requirements
        requirements = analyze_job_posting(job)
        
        # Tailor resume to job
        tailored = tailor_resume_to_job(
            master_resume=master_resume,
            job=job,
            requirements=requirements
        )
        
        tailored_resumes.append(tailored)
    
    return category_name, tailored_resumes

# Deploy agents in parallel
async def process_all_categories(categories_jobs_dict, master_resume):
    tasks = [
        process_category(cat, jobs, master_resume)
        for cat, jobs in categories_jobs_dict.items()
    ]
    results = await asyncio.gather(*tasks)
    return dict(results)
```

## Bundled Resources

This skill includes helpful reference files and scripts:

- **references/action-verbs.md**: Comprehensive action verbs organized by function (leadership, technical, marketing, etc.) for resume bullet points
- **references/ats-keywords.md**: Common ATS keywords organized by job category with usage guidelines
- **scripts/resume_tailor.py**: Complete Python implementation of the multi-agent coordination system

Load these references when needed for additional guidance.

## Step 5: Job Analysis Framework

Each agent analyzes job postings using this framework:

### Extract Key Elements

1. **Required Skills**: Must-have technical and soft skills
2. **Preferred Qualifications**: Nice-to-have skills/experience
3. **Action Verbs**: Verbs used to describe responsibilities (manage, develop, execute, etc.)
4. **Industry Keywords**: Domain-specific terminology (e.g., "brand voice," "engagement metrics," "project roadmap")
5. **ATS Keywords**: Repeated terms likely used for screening
6. **Responsibility Areas**: Main job functions (strategy, execution, reporting, etc.)
7. **Cultural Indicators**: Company values, work style clues

### Keyword Extraction Strategy

```python
def extract_keywords(job_description):
    """Extract ATS-relevant keywords"""
    # Tools/Technologies (exact matches important)
    tools = extract_proper_nouns(job_description)
    
    # Skills (with common variations)
    skills = extract_skill_phrases(job_description)
    
    # Action verbs (for experience descriptions)
    verbs = extract_action_verbs(job_description)
    
    # Industry terms (context-dependent)
    industry_terms = extract_domain_vocabulary(job_description)
    
    return {
        "tools": tools,
        "skills": skills,
        "action_verbs": verbs,
        "industry_terms": industry_terms
    }
```

## Step 6: Resume Tailoring Strategy

For each job posting, create a tailored resume following these principles:

### ONE-PAGE CONSTRAINT (CRITICAL)

**Every resume MUST fit on exactly one page. This is non-negotiable.**

To achieve this:
1. **Prioritize ruthlessly** - Include only the most relevant 2-3 positions
2. **Condense bullet points** - 2-4 bullets per position maximum
3. **Be concise** - Each bullet should be one line (max 2 lines)
4. **Remove less relevant sections** - If space is tight, remove:
   - Older positions (5+ years ago)
   - Unrelated work experience
   - Extensive project details
   - Unnecessary certifications
5. **Use efficient formatting**:
   - 10pt font minimum (11pt preferred for readability)
   - 0.5" margins all around (can go to 0.4" if absolutely necessary)
   - Single line spacing
   - Minimal white space between sections
6. **Strategic omissions** - It's better to omit less relevant content than exceed one page

### Professional Summary Tailoring

- **Mirror job title** in summary if applicable
- **Lead with most relevant skills** for this specific role
- **Include 2-3 keywords** from job description
- **Keep to 3-4 sentences** maximum

Example transformation:
```
Generic: "Digital marketing professional with 5 years of experience in content creation and social media."

Tailored for Social Media Manager role: "Social Media Marketing Strategist with 5 years of experience driving engagement across Instagram, TikTok, and LinkedIn. Proven track record in community management, content calendar development, and analytics-driven optimization. Skilled in Adobe Creative Suite and Hootsuite."
```

### Work Experience Tailoring

For each position in work history:

1. **Reorder bullet points** to prioritize most relevant achievements first
2. **Rewrite bullets** using action verbs from job description
3. **Quantify achievements** that match job requirements
4. **Add relevant details** from master resume that weren't in generic version
5. **Remove or minimize** less relevant responsibilities

**Key Principle**: Never fabricate experience, only emphasize what exists.

Example transformation:
```
Generic bullet:
"Managed social media accounts and created content"

Tailored for Social Media Manager (requires engagement metrics):
"Drove 150% increase in Instagram engagement through data-driven content strategy and community management across 3 brand accounts"

Tailored for Content Strategist (requires editorial process):
"Developed and maintained content calendar for 3 social platforms, coordinating with design and copywriting teams to ensure brand consistency"
```

### Skills Section Tailoring

1. **Prioritize skills from job description** at top of list
2. **Use exact phrasing** from job posting for tools/software
3. **Group skills** by relevance to role (Technical Skills, Marketing Tools, Soft Skills)
4. **Include certification details** if mentioned in job posting
5. **Remove unrelated skills** that could confuse ATS or distract

### Education & Additional Sections

- **Elevate relevant coursework, projects, or certifications** if specifically mentioned in job description
- **Reorder sections** to highlight most relevant credentials first
- **Add volunteer/project experience** if it demonstrates required skills

## Step 7: ATS Optimization Rules

Apply these rules to ALL tailored resumes:

### Format Requirements

- **Output format: PDF ONLY** - All resumes must be generated as PDF files
- **Page limit: EXACTLY ONE PAGE** - No exceptions
- **Use standard section headers**: Professional Summary, Work Experience, Education, Skills
- **Avoid tables, text boxes, headers/footers**: These confuse ATS parsers
- **Use standard fonts**: Arial, Calibri, Helvetica (10-11pt)
- **Use standard bullet points**: Simple circles or dashes only
- **Single column layout**: Multi-column layouts fail in many ATS systems
- **Margins**: 0.5" all around (can reduce to 0.4" if needed for space)
- **Line spacing**: Single spacing throughout
- **No graphics or images**: Text only for ATS compatibility

### Keyword Optimization

- **Match exact phrasing** from job description for tools/technologies (e.g., "Salesforce CRM" not "CRM software")
- **Include acronyms AND spelled-out versions** (e.g., "Search Engine Optimization (SEO)")
- **Use keywords naturally** in context, not just listed
- **Avoid keyword stuffing**: Aim for 2-3 mentions of critical keywords across resume
- **Include variations**: Different forms of important terms (e.g., "project management," "managed projects," "PM")

### Scanning Best Practices

- **Use quantifiable metrics**: Numbers and percentages pass through ATS
- **Spell out months**: "January 2020" not "Jan 2020" or "01/2020"
- **Avoid special characters**: Use plain text for better parsing
- **Use job titles from posting**: If you're a "Community Manager" applying for "Social Media Manager," use their title in summary

## Step 8: Output Organization

### Directory Structure

Create organized folders with clear naming:

```
tailored-resumes/
├── project-management/
│   ├── PM-CompanyA-Senior-PM.pdf
│   ├── PM-CompanyB-Technical-PM.pdf
│   └── PM-CompanyC-Agile-PM.pdf
├── social-media-marketing/
│   ├── SMM-CompanyA-Social-Media-Manager.pdf
│   ├── SMM-CompanyB-Community-Manager.pdf
│   └── SMM-CompanyC-Content-Manager.pdf
├── technical-writing/
│   ├── TW-CompanyA-Technical-Writer.pdf
│   └── TW-CompanyB-Documentation-Specialist.pdf
└── analysis-summary.md
```

### File Naming Convention

Format: `[CATEGORY-CODE]-[COMPANY]-[JOB-TITLE].pdf`

- **Category Code**: 2-4 letter abbreviation (PM, SMM, TW, etc.)
- **Company**: Abbreviated or shortened company name
- **Job Title**: Key words from position title

Examples:
- `SMM-Meta-Senior-Social-Manager.pdf`
- `PM-Google-Technical-Program-Manager.pdf`
- `CS-Polygon-Content-Strategist.pdf`

### Summary Report

Generate `analysis-summary.md` with:

```markdown
# Resume Tailoring Summary

**Master Resume**: [filename]
**Date**: [generation date]
**Total Resumes Generated**: [count]

## Categories Processed

### Social Media Marketing (10 resumes)
- Avg. keyword match: 87%
- Top skills emphasized: Instagram Analytics, Content Strategy, Community Management
- Companies: Meta, Twitter, LinkedIn, Buffer, Sprout Social...

### Project Management (8 resumes)
- Avg. keyword match: 82%
- Top skills emphasized: Agile, Stakeholder Management, Jira
- Companies: Google, Microsoft, Amazon, Salesforce...

## Recommendations

- Update master resume to include [missing skill found in multiple postings]
- Consider adding certification in [commonly requested qualification]
- Strong match for: [categories with highest keyword overlap]
```

## Step 9: Quality Assurance

Before finalizing, each tailored resume should pass these checks:

### Critical Requirements
- [ ] **EXACTLY ONE PAGE** - Not 0.9 pages, not 1.1 pages - exactly 1 page
- [ ] **PDF FORMAT** - File extension is .pdf
- [ ] PDF is readable and well-formatted

### Content Integrity
- [ ] No fabricated experience or skills
- [ ] All claims verifiable from master resume
- [ ] Dates and titles accurately preserved
- [ ] Contact information correct

### Optimization Checks
- [ ] Keywords from job description naturally integrated
- [ ] ATS-friendly formatting (single column, standard fonts)
- [ ] Professional summary mirrors job requirements
- [ ] Most relevant experience prioritized
- [ ] File named according to convention

### Readability & Formatting
- [ ] Clear section headers
- [ ] Consistent formatting throughout
- [ ] No spelling or grammar errors
- [ ] Adequate white space for readability (within one-page constraint)
- [ ] Font size is readable (minimum 10pt, prefer 11pt)

## Edge Cases & Troubleshooting

### Insufficient Matching Experience

If user's resume lacks key requirements for a job:
1. **Emphasize transferable skills** rather than leaving gaps
2. **Highlight learning ability** and related experience
3. **Add relevant coursework or self-study** if applicable
4. **Note in summary report** that this position may be a stretch

### Conflicting Job Requirements

If jobs in same category require different skill sets:
1. **Create distinct sub-categories** if appropriate
2. **Tailor each resume independently** rather than generalizing
3. **Prioritize most frequently requested skills** across similar roles

### ATS Parsing Failures

If certain elements cause ATS issues:
1. **Simplify formatting** progressively until parseable
2. **Remove special characters** and complex layouts
3. **Test with free ATS checkers** (Jobscan, Resume Worded)
4. **Default to plainest format** when unsure

## Best Practices

1. **Maintain truthfulness**: Only emphasize, never fabricate
2. **Preserve voice**: Keep user's writing style while optimizing
3. **Test iteratively**: Generate one resume, review with user, adjust approach
4. **Document patterns**: Track which keywords appear most often per category
5. **Version control**: Keep master resume separate and unmodified
6. **Batch processing**: Process all jobs in category before moving to next
7. **Error handling**: Gracefully handle missing data or malformed job postings

## User Interaction Flow

```
1. Confirm resume upload → Parse and validate
2. "What are your target job categories (3-5)?" → Collect categories
3. For each category: "Please provide job postings for [CATEGORY] (up to 10)"
4. "Analyzing [X] job postings across [Y] categories..."
5. [Progress updates as agents complete each category]
6. "Generated [Z] tailored resumes. See /tailored-resumes/ directory"
7. Present analysis-summary.md for review
```

## Performance Optimization

- **Parallel processing**: Deploy category agents simultaneously
- **Cache parsed resume**: Avoid re-parsing for each job
- **Batch similar jobs**: Group jobs with 80%+ requirement overlap
- **Limit context**: Pass only relevant resume sections to tailoring function
- **Async I/O**: Write files asynchronously while processing continues

## Success Metrics

Track and report:
- Keyword match percentage per resume
- Processing time per category
- Average tailoring depth (how many changes made)
- ATS compatibility score (if available via tools)
