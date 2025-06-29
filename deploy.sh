#!/bin/bash

# STL Weight Estimator API - Deployment Helper Script
# This script helps you prepare your code for deployment to Render

echo "🚀 STL Weight Estimator API - Deployment Helper"
echo "=============================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
else
    echo "✅ Git repository already initialized"
fi

# Check if files exist
echo "📋 Checking required files..."

required_files=("main.py" "requirements.txt" "render_start.py" "test.html" "README.md")

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing!"
        exit 1
    fi
done

echo ""
echo "📝 Current git status:"
git status

echo ""
echo "🔧 Next steps:"
echo "1. Add your files to git:"
echo "   git add ."
echo ""
echo "2. Commit your changes:"
echo "   git commit -m 'Initial commit: STL Weight Estimator API'"
echo ""
echo "3. Create a new repository on GitHub:"
echo "   - Go to https://github.com/new"
echo "   - Choose a repository name"
echo "   - Make it public or private"
echo "   - Don't initialize with README (we already have one)"
echo ""
echo "4. Connect to GitHub (replace YOUR_USERNAME and REPO_NAME):"
echo "   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "5. Deploy to Render:"
echo "   - Go to https://render.com"
echo "   - Sign up with GitHub"
echo "   - Create new Web Service"
echo "   - Select your repository"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: python render_start.py"
echo ""
echo "📖 For detailed instructions, see DEPLOYMENT.md"
echo ""
echo "🎉 Good luck with your deployment!" 