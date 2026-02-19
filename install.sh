#!/bin/bash

# Resume Tailor Skill - Installation Script
# This script helps you install the Resume Tailor skill for Claude Code

set -e  # Exit on error

echo "════════════════════════════════════════════════════════════"
echo "  Resume Tailor Skill - Installation for Claude Code"
echo "════════════════════════════════════════════════════════════"
echo ""

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)

# Determine Claude Code skills directory
CLAUDE_SKILLS_DIR=""

if [[ "$OS" == "macos" ]] || [[ "$OS" == "linux" ]]; then
    # Common locations for Claude Code skills
    if [ -d "$HOME/.claude/skills/user" ]; then
        CLAUDE_SKILLS_DIR="$HOME/.claude/skills/user"
    elif [ -d "$HOME/.config/claude/skills/user" ]; then
        CLAUDE_SKILLS_DIR="$HOME/.config/claude/skills/user"
    else
        echo "⚠️  Could not find Claude Code skills directory."
        echo "    Please enter the path manually:"
        read -p "    Skills directory path: " CLAUDE_SKILLS_DIR
        
        # Create directory if it doesn't exist
        if [ ! -d "$CLAUDE_SKILLS_DIR" ]; then
            echo "    Creating directory: $CLAUDE_SKILLS_DIR"
            mkdir -p "$CLAUDE_SKILLS_DIR"
        fi
    fi
else
    echo "⚠️  Windows detected. Please manually copy the 'resume-tailor' folder to:"
    echo "    %USERPROFILE%\\.claude\\skills\\user\\"
    exit 1
fi

echo "📁 Claude Code skills directory: $CLAUDE_SKILLS_DIR"
echo ""

# Check if Python is installed
echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    echo "   Visit: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✓ Found: $PYTHON_VERSION"
echo ""

# Check if pip is installed
echo "🔍 Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi
echo "✓ pip is installed"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
echo "   (anthropic, python-docx, pdfplumber)"
echo ""

pip3 install -r requirements.txt --break-system-packages || {
    echo "⚠️  Installation with --break-system-packages failed."
    echo "   Trying without flag..."
    pip3 install -r requirements.txt
}

echo ""
echo "✓ Python dependencies installed"
echo ""

# Copy skill to Claude Code directory
SKILL_NAME="resume-tailor"
DEST_DIR="$CLAUDE_SKILLS_DIR/$SKILL_NAME"

echo "📋 Installing skill to Claude Code..."
echo "   Destination: $DEST_DIR"
echo ""

# Check if skill already exists
if [ -d "$DEST_DIR" ]; then
    echo "⚠️  Skill already exists at destination."
    read -p "   Overwrite? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Installation cancelled."
        exit 1
    fi
    echo "   Removing existing installation..."
    rm -rf "$DEST_DIR"
fi

# Copy files (excluding this script, git files, and output directories)
echo "   Copying skill files..."
cp -r . "$DEST_DIR"

# Clean up installation script and git files from destination
rm -f "$DEST_DIR/install.sh"
rm -rf "$DEST_DIR/.git"
rm -f "$DEST_DIR/.gitignore"

echo "✓ Skill files copied"
echo ""

# Make Python script executable
chmod +x "$DEST_DIR/scripts/resume_tailor.py"

echo "════════════════════════════════════════════════════════════"
echo "  ✅ Installation Complete!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Start Claude Code in your terminal"
echo "2. Say: 'I need to tailor my resume for multiple jobs'"
echo "3. The skill will automatically activate!"
echo ""
echo "Or run the script directly:"
echo "   cd $DEST_DIR/scripts"
echo "   python3 resume_tailor.py --resume /path/to/your/resume.docx"
echo ""
echo "📚 Documentation: See README.md for full instructions"
echo "🐛 Issues? Visit: https://github.com/platonic-canine-lover/resume-tailor-skill/issues"
echo ""
echo "Good luck with your job search! 🚀"
echo ""
