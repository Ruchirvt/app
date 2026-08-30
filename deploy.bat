@echo off
echo 🌤️ SkyCast AI Deployment Script
echo ================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed. Please install Git first.
    pause
    exit /b 1
)

set /p username="Enter your GitHub username: "
set /p repo_name="Enter repository name (default: skycast-ai): "
if "%repo_name%"=="" set repo_name=skycast-ai

echo.
echo 🚀 Setting up repository...

git init
git add .
git commit -m "🌤️ Initial commit - SkyCast AI Weather App"
git branch -M main
git remote add origin https://github.com/%username%/%repo_name%.git

echo.
echo 📤 Pushing to GitHub...
git push -u origin main

echo.
echo ✅ Done! Your code is now on GitHub.
echo.
echo Next steps:
echo 1. Go to https://share.streamlit.io
echo 2. Sign in with GitHub
echo 3. Click 'New app'
echo 4. Select: %username%/%repo_name%
echo 5. Set Main file path: app.py
echo 6. Click Deploy! 🚀
echo.
pause
