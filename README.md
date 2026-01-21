# Resume Tailor - Multi-Agent Claude Skill

A Claude Code skill that uses multiple AI agents to automatically generate tailored, ATS-optimized **ONE-PAGE PDF resumes** for dozens of job applications at once.

## 🎯 What It Does

Upload your master resume once, specify 3-5 job categories, provide up to 10 job postings per category, and let parallel AI agents create customized resumes for each position. Each resume is:

- ✅ **EXACTLY ONE PAGE** - Ruthlessly prioritized and concise
- ✅ **PDF FORMAT ONLY** - Professional, ready-to-submit PDFs
- ✅ **ATS-optimized** with keywords from the job description
- ✅ **Truthful** - only emphasizes existing experience, never fabricates
- ✅ **Professionally formatted** with single-column layout and standard fonts
- ✅ **Organized** in category-based folders with clear naming

Perfect for job seekers applying to multiple roles across different specializations (e.g., Social Media Marketing, Project Management, Content Strategy).

## 🚀 Quick Start

### Prerequisites

- [Claude Code](https://claude.ai/code) installed
- Python 3.8+
- Anthropic API key (for standalone script usage)

### Installation

#### Option 1: For Claude Code (Recommended)

1. **Download this skill**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/resume-tailor-skill.git
   cd resume-tailor-skill
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt --break-system-packages
   ```
   
   Dependencies:
   - `anthropic` - Claude API
   - `python-docx` - Parse DOCX resumes
   - `pdfplumber` - Parse PDF resumes
   - `reportlab` - Generate PDF output

3. **Copy to Claude Code skills directory**:
   
   **macOS/Linux**:
   ```bash
   # Find your Claude Code skills directory (usually ~/.claude/skills or similar)
   # Copy the entire resume-tailor folder there
   cp -r resume-tailor ~/.claude/skills/user/
   ```
   
   **Windows**:
   ```powershell
   # Copy to your Claude Code skills directory
   Copy-Item -Recurse resume-tailor "$env:USERPROFILE\.claude\skills\user\"
   ```

4. **Use in Claude Code**:
   ```bash
   # Start Claude Code and say:
   "I need to tailor my resume for multiple job applications"
   ```
   
   The skill will automatically activate and guide you through the process!

#### Option 2: Standalone Script

If you want to run the script directly without Claude Code:

```bash
# Install dependencies
pip install -r requirements.txt --break-system-packages

# Run the script
python scripts/resume_tailor.py --resume /path/to/your/resume.docx
```

## 📖 How It Works

```
Master Resume → Parse → Categories → Job Postings → Multi-Agent Analysis → Tailored Resumes
```

### The Process

1. **Upload your master resume** (.docx or .pdf)
2. **Specify 3-5 job categories** you're targeting
3. **Provide up to 10 job postings per category** (paste descriptions or URLs)
4. **AI agents process in parallel**:
   - One agent per category
   - Each analyzes all jobs in its category
   - Extracts keywords, requirements, and action verbs
   - Tailors your resume to match each specific job
5. **Receive organized output**:
   ```
   tailored-resumes/
   ├── social-media-marketing/
   │   ├── SMM-Meta-Social-Media-Manager.pdf
   │   ├── SMM-Buffer-Community-Manager.pdf
   │   └── ...
   ├── project-management/
   │   ├── PM-Google-Technical-PM.pdf
   │   └── ...
   └── analysis-summary.md
   ```

## 🎨 Features

### Critical Requirements
- **One-Page PDFs**: Every resume is exactly one page - no more, no less
- **PDF Only**: All output in professional PDF format, ready to submit

### Multi-Agent Coordination
- **Parallel processing**: Multiple agents work simultaneously on different categories
- **Specialized analysis**: Each agent becomes an expert in its category
- **Efficient**: Process 50+ jobs in minutes instead of hours

### ATS Optimization
- **Keyword matching**: Extracts and uses exact phrases from job descriptions
- **Format compliance**: Single-column, standard fonts, no graphics/tables
- **Section headers**: Uses ATS-friendly standard headers
- **Metric-focused**: Prioritizes quantifiable achievements

### Truthful Tailoring
- **Never fabricates**: Only emphasizes and reorders existing content
- **Preserves accuracy**: All dates, titles, and facts remain unchanged
- **Smart prioritization**: Most relevant experience appears first
- **Voice preservation**: Maintains your writing style

### Intelligent Analysis
- **Keyword extraction**: Identifies tools, technologies, and methodologies
- **Requirements mapping**: Matches your experience to job requirements
- **Action verb selection**: Uses verbs from the job description
- **Cultural indicators**: Notes company values and work style

## 📁 What's Included

### Core Files

- **`SKILL.md`** (15KB) - Complete workflow instructions for Claude Code
- **`scripts/resume_tailor.py`** (14KB) - Fully functional Python implementation
- **`requirements.txt`** - Python dependencies

### Reference Materials

- **`references/action-verbs.md`** (7KB) - Hundreds of action verbs organized by function
- **`references/ats-keywords.md`** (11KB) - ATS keywords by job category

### Supported Job Categories

The skill includes optimized keywords for:
- Project Management (Agile, Scrum, Jira, Stakeholder Management)
- Social Media Marketing (Instagram, TikTok, Community Management, Analytics)
- Content Strategy (SEO, Copywriting, Editorial Calendars)
- Software Engineering (React, Python, AWS, Microservices)
- Data Analytics (SQL, Tableau, A/B Testing)
- Web3/Blockchain (DeFi, Smart Contracts, Tokenomics, DAOs)
- Sales & Business Development
- Design (UX/UI)
- Customer Success

## 🎯 Example Usage

### In Claude Code

```
You: "I need tailored resumes for social media and project management roles"

Claude Code: "I'll help you create tailored resumes using the Resume Tailor skill.
              First, please upload your master resume."

[You upload resume.docx]

Claude Code: "Got it! I see you want resumes for Social Media and Project Management.
              Any other categories? (You can specify 3-5 total)"

You: "Also add Content Strategy"

Claude Code: "Perfect! Now let's collect job postings.
              
              For Social Media Marketing, please provide up to 10 job postings.
              You can paste descriptions, provide URLs, or upload files."

[You paste 8 job descriptions]

Claude Code: "Great! Processing 8 Social Media Marketing roles...
              Now for Project Management..."

[Process repeats for each category]

Claude Code: "🤖 Deploying 3 agents to process your 24 job postings...
              
              ✓ Social Media Marketing agent: 8 resumes complete
              ✓ Project Management agent: 10 resumes complete  
              ✓ Content Strategy agent: 6 resumes complete
              
              Generated 24 tailored resumes!
              See: tailored-resumes/ directory"
```

### Standalone Script

```bash
$ python scripts/resume_tailor.py --resume my-resume.docx

=== Resume Tailor - Multi-Agent System ===

Loading resume: my-resume.docx
✓ Resume loaded successfully

--- Job Categories ---
Enter 3-5 job categories you're targeting
Examples: 'Project Management', 'Social Media Marketing', 'Content Strategy'

Category 1 (press Enter to finish): Social Media Marketing
Category 2 (press Enter to finish): Project Management
Category 3 (press Enter to finish): 

--- Collecting jobs for: Social Media Marketing ---
Provide up to 10 job postings (paste description or URL)

Job 1 (or type 'done' to finish):
  Company name: Meta
  Job title: Social Media Manager
  URL (optional): https://...
  Job description (paste below, type 'END' on new line when done):
[Paste description]
END

...

🤖 Deploying agents to process job categories...
  Analyzing: Meta - Social Media Manager
  Tailoring resume for: Meta - Social Media Manager
  ...

✓ Saved 18 tailored resumes to tailored-resumes/

✅ Resume tailoring complete!
```

## 🛠️ Customization

### Add Your Own Keywords

Edit `references/ats-keywords.md` to add industry-specific terms:

```markdown
## Your Industry

### Core Skills
- Skill 1, Skill 2, Skill 3

### Tools
- Tool A, Tool B, Tool C
```

### Modify Tailoring Rules

Edit `scripts/resume_tailor.py` to change how resumes are tailored:

```python
def tailor_resume(self, job: JobPosting, job_analysis: Dict[str, Any]) -> str:
    """Customize this function to change tailoring behavior"""
    prompt = f"""Your custom prompt here..."""
    # ... rest of function
```

### Add New Resume Sections

Modify the `ResumeData` dataclass in `resume_tailor.py`:

```python
@dataclass
class ResumeData:
    contact_info: Dict[str, str]
    summary: str
    experience: List[Dict[str, Any]]
    education: List[Dict[str, Any]]
    skills: List[str]
    certifications: List[str]  # Add new section
    publications: List[str]     # Add new section
```

## 💡 Best Practices

### For Your Master Resume

Include:
- ✅ ALL relevant work experience (even if not always used)
- ✅ Quantified achievements with specific metrics
- ✅ Complete technical and soft skills
- ✅ All certifications and education
- ✅ Projects, volunteering, publications
- ✅ Different phrasings of similar skills (for keyword matching)

### For Job Categories

Be specific:
- ✅ "Social Media Marketing" not just "Marketing"
- ✅ "Technical Project Management" not just "Project Management"
- ✅ "Content Strategy" not just "Writing"

More specific categories = better tailoring

### For Job Descriptions

Provide complete information:
- ✅ Full job description text (not just a link)
- ✅ Include requirements, responsibilities, and qualifications sections
- ✅ Copy any special keywords or phrases exactly
- ❌ Don't just paste the job title and company

## 🔧 Troubleshooting

**Issue**: Import errors when running script  
**Solution**: `pip install anthropic python-docx pdfplumber --break-system-packages`

**Issue**: Skill not triggering in Claude Code  
**Solution**: Ensure skill is in correct directory (usually `~/.claude/skills/user/`)

**Issue**: ATS rejects resume  
**Solution**: Check for: single-column layout, standard fonts (Arial/Calibri), no tables/text boxes, standard section headers

**Issue**: Missing relevant experience  
**Solution**: Add missing details to your master resume and re-run

**Issue**: Keywords not matching  
**Solution**: Ensure full job description was pasted; the more context, the better the keyword extraction

## 📄 License

MIT License - Feel free to use, modify, and share!

## 🤝 Contributing

Contributions welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Ideas for Contributions

- Add support for more resume formats (LaTeX, HTML)
- Create templates for specific industries
- Add more job categories to `ats-keywords.md`
- Improve keyword extraction algorithms
- Add resume scoring/optimization suggestions
- Build a web interface

## 🙏 Acknowledgments

Created to help job seekers efficiently apply to multiple positions while maintaining quality and honesty in their applications.

Special thanks to the Anthropic team for Claude and the multi-agent capabilities that make this possible.

## 📬 Contact

Questions? Issues? Feedback?

- Open an issue on GitHub
- Star ⭐ this repo if it helps you land interviews!

---

**Note**: This skill uses the Anthropic API. You'll need an API key for the standalone script. When using with Claude Code, authentication is handled automatically.

**Good luck with your job search!** 🚀
