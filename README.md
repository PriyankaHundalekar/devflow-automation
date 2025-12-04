DevFlow Automator 🚀
Stars Issues License Last Commit

A comprehensive Streamlit web app that automates the most annoying developer workflows using AWS AI. Stop wasting time on repetitive tasks and focus on what matters - building great software.

✨ Features
🤖 AI-Powered Commit Messages
Analyzes your git changes and generates meaningful commit messages using AWS Bedrock AI.

🏷️ Smart Badge Management
Auto-updates README badges for build status, version, license, and more.

🏗️ AI Code Generator
Generate custom code from natural language descriptions using AWS Claude.

📚 Project Setup
Bootstrap new projects (Python Flask/FastAPI, Node.js, React) with best practices.

📊 Git Analytics
Analyze repository statistics, commit history, and file change patterns.

🛠️ Installation & Setup
Clone the repository
git clone https://github.com/PriyankaHundalekar/devflow-automation.git
cd devflow-automation
Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
Install dependencies
pip install -r requirements.txt
Set up AWS credentials Your .env file is already created with your AWS credentials.

Test the setup

python test_app.py
Run the app
streamlit run app.py
🎯 Quick Start
Launch the app
streamlit run app.py
Open your browser to http://localhost:8501

Choose a tool from the sidebar:

🤖 AI Commit Messages - Generate smart commit messages
🏷️ Badge Manager - Update README badges
🏗️ Code Generator - Create code from descriptions
📚 Project Setup - Bootstrap new projects
📊 Git Analytics - Analyze repository stats
🧪 Testing Your Setup
Run the test script to verify everything works:

python test_app.py
This will check:

✅ All required packages are installed
✅ AWS credentials are configured
✅ AWS Bedrock connection works
✅ Git repository detection (optional)
📋 Available Tools
Tool	Description	What it does
🤖 AI Commit Messages	Smart commit generation	Analyzes git changes and creates conventional commit messages
🏷️ Badge Manager	README badge automation	Generates and updates GitHub badges in README
🏗️ Code Generator	AI-powered coding	Creates code from natural language descriptions
📚 Project Setup	Project bootstrapping	Sets up Python/Node.js/React projects with best practices
📊 Git Analytics	Repository insights	Shows commit history, file changes, and repo statistics
🔧 Configuration
AWS Bedrock Setup
This tool uses AWS Bedrock for AI capabilities. Make sure you have:

AWS account with Bedrock access
Claude 3 Haiku model enabled in your region
Proper IAM permissions for Bedrock
Supported Project Types
Python: Flask, FastAPI, Django
JavaScript: Node.js, Express, React
TypeScript: React, Node.js
General: Git repositories, documentation
🎨 Screenshots & Examples
🤖 AI Commit Messages
The app analyzes your git changes and suggests conventional commit messages:

Detects staged and unstaged changes
Uses AWS Claude AI for intelligent analysis
Supports custom message editing
One-click commit functionality
🏗️ Code Generator
Generate code from natural language:

"Create a user authentication system"
"Build a REST API endpoint for users"
"Make a file upload handler"
Save generated code directly to files
📚 Project Setup
Bootstrap complete projects:

Python Flask: Web app with routes, error handling
Python FastAPI: Modern API with automatic docs
Node.js Express: Server with middleware setup
React App: Component structure with modern practices
🤝 Contributing
Fork the repository
Create a feature branch
Make your changes
Add tests if applicable
Submit a pull request
📄 License
MIT License - see LICENSE for details.

🏆 Kiro Hero Week 2 Challenge
This project was built for the Kiro Hero Week 2 Challenge with the theme "Lazy Automation". It demonstrates how AI can be used to automate repetitive developer tasks, saving time and reducing cognitive load.

Challenge Requirements Met:

✅ Automates boring digital tasks
✅ Uses creative problem-solving
✅ Includes .kiro file
✅ Comprehensive documentation
✅ Real-world utility
Built with ❤️ and a healthy dose of laziness
