#!/bin/bash

# Git Setup Script for AI Operations Assistant
# This script initializes git and prepares the repository for submission

echo "=========================================="
echo "Git Repository Setup"
echo "=========================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

echo "✓ Git is installed"

# Initialize git repository
if [ -d .git ]; then
    echo "⚠️  Git repository already exists"
else
    echo "📦 Initializing git repository..."
    git init
    echo "✓ Git initialized"
fi

# Check if .env exists and warn
if [ -f .env ]; then
    echo "⚠️  WARNING: .env file exists"
    echo "   This file contains your API keys and should NOT be committed"
    echo "   Make sure .gitignore is working correctly"
fi

# Add all files
echo "📝 Adding files to git..."
git add .

# Show status
echo ""
echo "📊 Git status:"
git status

# Create initial commit
echo ""
read -p "Create initial commit? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git commit -m "Initial commit: AI Operations Assistant

Multi-agent AI system for TrulyMadly GenAI Intern assignment

Features:
- Planner, Executor, and Verifier agents
- OpenAI LLM with structured outputs
- GitHub, Weather, and News API integrations
- FastAPI server with Swagger UI
- Comprehensive documentation"
    
    echo "✓ Initial commit created"
fi

echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Create a new repository on GitHub:"
echo "   https://github.com/new"
echo ""
echo "2. Add remote and push:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/ai-ops-assistant.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Make repository public or share access"
echo ""
echo "4. Submit the GitHub link:"
echo "   https://forms.gle/YjoQcqhuhr3w5XtHA"
echo ""
echo "=========================================="
