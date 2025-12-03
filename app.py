"""
DevFlow Automator - Streamlit Web App
"I hate doing repetitive dev tasks, so I built this"
"""

# importing libraries needed for project 

import streamlit as st
import subprocess
import json
import os
import re
from pathlib import Path
from aws_client import AWSAIClient
import git

# Page configs
st.set_page_config(
    page_title="DevFlow Automator",
    page_icon="🚀",
    layout="wide"
)

# Initialize AI client
@st.cache_resource
def get_ai_client():
    return AWSAIClient()

def main():
    st.title("🚀 DevFlow Automator")
    st.markdown("*I hate doing repetitive dev tasks, so I built this*")
    
    # Sidebar navigation
    st.sidebar.title("🛠️ Tools")
    tool = st.sidebar.selectbox(
        "Choose a tool:",
        ["🤖 AI Commit Messages", "🏷️ Badge Manager", "🏗️ Code Generator", "📚 Project Setup", "📊 Git Analytics"]
    )
    
    if tool == "🤖 AI Commit Messages":
        commit_message_tool()
    elif tool == "🏷️ Badge Manager":
        badge_manager_tool()
    elif tool == "🏗️ Code Generator":
        code_generator_tool()
    elif tool == "📚 Project Setup":
        project_setup_tool()
    elif tool == "📊 Git Analytics":
        git_analytics_tool()

def commit_message_tool():
    st.header("🤖 AI-Powered Commit Messages")
    st.markdown("Generate meaningful commit messages from your git changes")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🔍 Analyze Current Changes", type="primary"):
            try:
                # Get git diff
                result = subprocess.run(['git', 'diff', '--cached'], 
                                      capture_output=True, text=True)
                if not result.stdout.strip():
                    result = subprocess.run(['git', 'diff'], 
                                          capture_output=True, text=True)
                
                diff = result.stdout
                
                if not diff:
                    st.warning("No git changes found. Make some changes first!")
                    return
                
                st.success("📊 Changes detected! Generating commit message...")
                
                # Generate commit message
                ai_client = get_ai_client()
                commit_message = ai_client.analyze_code_changes(diff)
                
                st.subheader("🎯 Suggested Commit Message")
                st.code(commit_message, language="text")
                
                # Show diff preview
                with st.expander("📄 View Changes"):
                    st.code(diff[:2000] + "..." if len(diff) > 2000 else diff, language="diff")
                
                # Commit options
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✅ Use This Message"):
                        try:
                            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
                            st.success("🎉 Committed successfully!")
                        except subprocess.CalledProcessError as e:
                            st.error(f"❌ Commit failed: {e}")
                
                with col_b:
                    custom_message = st.text_input("Or edit the message:")
                    if custom_message and st.button("📝 Commit Custom"):
                        try:
                            subprocess.run(['git', 'commit', '-m', custom_message], check=True)
                            st.success("🎉 Committed successfully!")
                        except subprocess.CalledProcessError as e:
                            st.error(f"❌ Commit failed: {e}")
                            
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    with col2:
        st.info("💡 **Tips:**\n- Stage your changes with `git add`\n- Or just make changes and we'll detect them\n- Uses conventional commit format")

def badge_manager_tool():
    st.header("🏷️ README Badge Manager")
    st.markdown("Auto-generate and update README badges")
    
    # Get repository info
    try:
        repo = git.Repo('.')
        
        # Check if origin remote exists
        if 'origin' not in repo.remotes:
            st.warning("⚠️ No 'origin' remote found. Add one to use Badge Manager:")
            st.code("git remote add origin https://github.com/username/repo-name.git")
            return
        
        remote_url = repo.remotes.origin.url
        
        # Parse GitHub URL
        match = re.search(r'github\.com[:/]([^/]+)/([^/.]+)', remote_url)
        if match:
            user, repo_name = match.groups()
            st.success(f"📦 Detected repository: **{user}/{repo_name}**")
            
            # Badge selection
            st.subheader("🎯 Select Badges")
            
            badges = {
                'Build Status': f'![Build Status](https://img.shields.io/github/actions/workflow/status/{user}/{repo_name}/ci.yml?branch=main)',
                'Version': f'![Version](https://img.shields.io/github/package-json/v/{user}/{repo_name})',
                'License': f'![License](https://img.shields.io/github/license/{user}/{repo_name})',
                'Issues': f'![Issues](https://img.shields.io/github/issues/{user}/{repo_name})',
                'Forks': f'![Forks](https://img.shields.io/github/forks/{user}/{repo_name})',
                'Stars': f'![Stars](https://img.shields.io/github/stars/{user}/{repo_name})',
                'Last Commit': f'![Last Commit](https://img.shields.io/github/last-commit/{user}/{repo_name})',
                'Code Size': f'![Code Size](https://img.shields.io/github/languages/code-size/{user}/{repo_name})'
            }
            
            selected_badges = []
            col1, col2 = st.columns(2)
            
            for i, (name, markdown) in enumerate(badges.items()):
                col = col1 if i % 2 == 0 else col2
                if col.checkbox(name):
                    selected_badges.append(markdown)
            
            if selected_badges:
                st.subheader("🎨 Generated Badge Markdown")
                badge_markdown = ' '.join(selected_badges)
                st.code(badge_markdown, language="markdown")
                
                if st.button("📝 Update README", type="primary"):
                    update_readme_badges(badge_markdown)
        else:
            st.error("❌ Could not detect GitHub repository")
            
    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.info("Make sure you're in a git repository with GitHub remote")

def update_readme_badges(badge_markdown):
    """Update README.md with badges"""
    try:
        readme_path = Path('README.md')
        
        if not readme_path.exists():
            st.error("❌ README.md not found")
            return
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for existing badge section
        badge_pattern = r'(<!-- BADGES START -->.*?<!-- BADGES END -->)'
        badge_section = f"<!-- BADGES START -->\n{badge_markdown}\n<!-- BADGES END -->"
        
        if re.search(badge_pattern, content, re.DOTALL):
            content = re.sub(badge_pattern, badge_section, content, flags=re.DOTALL)
            st.info("🔄 Updated existing badge section")
        else:
            # Add badges at the top after title
            lines = content.split('\n')
            if lines and lines[0].startswith('#'):
                lines.insert(2, badge_section)
                lines.insert(2, '')
                content = '\n'.join(lines)
            else:
                content = badge_section + '\n\n' + content
            st.info("➕ Added new badge section")
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        st.success("✅ README.md updated successfully!")
        
    except Exception as e:
        st.error(f"❌ Error updating README: {e}")

def code_generator_tool():
    st.header("🏗️ AI Code Generator")
    st.markdown("Generate code from natural language descriptions")
    
    description = st.text_area(
        "📝 Describe what you want to build:",
        placeholder="e.g., Create a user authentication system with login and registration",
        height=100
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("🤖 Generate Code", type="primary") and description:
            with st.spinner("🔄 Generating code..."):
                ai_client = get_ai_client()
                code = ai_client.generate_code(description)
                
                st.subheader("🎯 Generated Code")
                st.code(code, language="python")
                
                # Save option
                filename = st.text_input("💾 Save as (optional):", placeholder="my_code.py")
                if filename and st.button("💾 Save File"):
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(code)
                    st.success(f"✅ Saved to {filename}")
    
    with col2:
        st.info("💡 **Examples:**\n- REST API endpoint\n- Database model\n- Authentication system\n- File processor\n- Web scraper")

def project_setup_tool():
    st.header("📚 Project Setup")
    st.markdown("Bootstrap new projects with best practices")
    
    project_type = st.selectbox(
        "🎯 Choose project type:",
        ["Python Flask", "Python FastAPI", "Node.js Express", "React App"]
    )
    
    project_name = st.text_input("📝 Project name:", placeholder="my-awesome-project")
    
    if st.button("🚀 Create Project", type="primary") and project_name:
        create_project(project_type, project_name)

def create_project(project_type, project_name):
    """Create project structure"""
    try:
        # Create project directory
        project_path = Path(project_name)
        project_path.mkdir(exist_ok=True)
        
        templates = {
            "Python Flask": {
                "app.py": '''from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({"message": "Hello World!"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True)''',
                "requirements.txt": "flask>=2.3.0\npython-dotenv>=1.0.0\nrequests>=2.31.0",
                ".env.example": "DEBUG=True\nAPI_KEY=your_api_key",
                ".gitignore": "__pycache__/\n*.pyc\n.env\nvenv/\n*.log"
            },
            
            "Python FastAPI": {
                "main.py": '''from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="My API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}''',
                "requirements.txt": "fastapi>=0.104.0\nuvicorn>=0.24.0\npython-dotenv>=1.0.0",
                ".env.example": "DEBUG=True\nAPI_KEY=your_api_key",
                ".gitignore": "__pycache__/\n*.pyc\n.env\nvenv/\n.pytest_cache/"
            },
            
            "Node.js Express": {
                "package.json": '''{
  "name": "''' + project_name + '''",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js"
  },
  "dependencies": {
    "express": "^4.18.0",
    "dotenv": "^16.0.0"
  }
}''',
                "index.js": '''const express = require('express');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.json({ message: 'Hello World!' });
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});''',
                ".env.example": "PORT=3000\nNODE_ENV=development",
                ".gitignore": "node_modules/\n.env\n*.log"
            },
            
            "React App": {
                "package.json": '''{
  "name": "''' + project_name + '''",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test"
  }
}''',
                "public/index.html": '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>React App</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>''',
                "src/index.js": '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);''',
                "src/App.js": '''import React from 'react';

function App() {
  return (
    <div className="App">
      <h1>Hello React!</h1>
      <p>Welcome to your new React app!</p>
    </div>
  );
}

export default App;''',
                ".gitignore": "node_modules/\nbuild/\n.env\n*.log"
            }
        }
        
        # Create files
        template = templates[project_type]
        for file_path, content in template.items():
            full_path = project_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        st.success(f"🎉 Project '{project_name}' created successfully!")
        st.info(f"📁 Created in: {project_path.absolute()}")
        
        # Show next steps
        st.subheader("📋 Next Steps")
        if "Python" in project_type:
            st.code(f"""cd {project_name}
python -m venv venv
venv\\Scripts\\activate  # Windows
pip install -r requirements.txt
python {"main.py" if "FastAPI" in project_type else "app.py"}""")
        else:
            st.code(f"""cd {project_name}
npm install
npm start""")
            
    except Exception as e:
        st.error(f"❌ Error creating project: {e}")

def git_analytics_tool():
    st.header("📊 Git Analytics")
    st.markdown("Analyze your repository statistics")
    
    try:
        repo = git.Repo('.')
        
        # Basic repo info
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📁 Current Branch", repo.active_branch.name)
        
        with col2:
            commits = list(repo.iter_commits())
            st.metric("📝 Total Commits", len(commits))
        
        with col3:
            remotes = len(repo.remotes)
            st.metric("🔗 Remotes", remotes)
        
        # Recent commits
        st.subheader("📈 Recent Commits")
        recent_commits = list(repo.iter_commits(max_count=10))
        
        for commit in recent_commits:
            with st.expander(f"🔸 {commit.summary[:50]}..."):
                st.write(f"**Author:** {commit.author}")
                st.write(f"**Date:** {commit.committed_datetime}")
                st.write(f"**Hash:** `{commit.hexsha[:8]}`")
                st.write(f"**Message:** {commit.message}")
        
        # File changes
        if st.button("🔍 Analyze File Changes"):
            file_stats = {}
            for commit in repo.iter_commits(max_count=100):
                for item in commit.stats.files:
                    if item not in file_stats:
                        file_stats[item] = 0
                    file_stats[item] += 1
            
            if file_stats:
                st.subheader("📊 Most Modified Files")
                sorted_files = sorted(file_stats.items(), key=lambda x: x[1], reverse=True)[:10]
                
                for file_path, count in sorted_files:
                    st.write(f"📄 **{file_path}**: {count} changes")
                    
    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.info("Make sure you're in a git repository")

if __name__ == "__main__":
    main()