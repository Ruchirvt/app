#!/bin/bash
# SkyCast AI - GitHub & Streamlit Deployment Helper

echo "🌤️ SkyCast AI Deployment Script"
echo "================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Get GitHub username
echo "Enter your GitHub username:"
read username

echo "Enter your repository name (default: skycast-ai):"
read repo_name
repo_name=${repo_name:-skycast-ai}

echo ""
echo "🚀 Setting up repository..."

# Initialize git if not already
git init

# Add all files
git add .

# Commit
git commit -m "🌤️ Initial commit - SkyCast AI Weather App"

# Rename branch
git branch -M main

# Add remote
git remote add origin https://github.com/$username/$repo_name.git

# Push
echo ""
echo "📤 Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Done! Your code is now on GitHub."
echo ""
echo "Next steps:"
echo "1. Go to https://share.streamlit.io"
echo "2. Sign in with GitHub"
echo "3. Click 'New app'"
echo "4. Select: $username/$repo_name"
echo "5. Set Main file path: app.py"
echo "6. Click Deploy! 🚀"
echo ""
echo "Your app will be live at: https://$repo_name-xxx.streamlit.app"
