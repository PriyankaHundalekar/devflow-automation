"""
DevFlow Automator - Streamlit Web App
"I hate doing repetitive dev tasks, so I built this"
"""

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
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for stunning UI with better contrast
st.markdown("""
<style>
    /* Main background - Elegant gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar styling - Dark elegant */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    }
    
    [data-testid="stSidebar"] .stSelectbox label {
        color: #ffffff !important;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Main content area - Full width */
    .main .block-container {
        background: #ffffff;
        border-radius: 0;
        padding: 3rem 4rem;
        box-shadow: none;
        max-width: 100%;
        margin: 0;
        overflow-x: hidden;
    }
    
    /* Headers - Clean and bold */
    h1 {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        color: #1a202c !important;
        font-weight: 700 !important;
        border-bottom: 4px solid #667eea;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
        font-size: 2.2rem !important;
    }
    
    h3 {
        color: #1a202c !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }
    
    /* Larger labels */
    label {
        font-size: 1.2rem !important;
    }
    
    /* Larger text in general */
    p {
        font-size: 1.15rem !important;
    }
    
    /* Buttons - Vibrant and professional */
    .stButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white !important;
        border: none;
        border-radius: 14px;
        padding: 1.1rem 2.5rem;
        font-weight: 800;
        font-size: 1.15rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.5);
        letter-spacing: 0.8px;
        text-transform: uppercase;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 12px 35px rgba(16, 185, 129, 0.7);
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(1.01);
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 5px solid #3182ce;
        background: #e6f2ff;
        color: #1a202c !important;
    }
    
    .stAlert p {
        color: #1a202c !important;
    }
    
    /* Code blocks */
    .stCodeBlock {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 0.9rem;
        transition: all 0.3s ease;
        background: white;
        color: #1a202c;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15);
    }
    
    .stTextInput label {
        color: #1a202c !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        background: white;
    }
    
    .stSelectbox label {
        color: #1a202c !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #e6f2ff;
        border-radius: 10px;
        font-weight: 600;
        color: #1a202c !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #3182ce;
    }
    
    /* Success/Error messages - Professional blue */
    .stSuccess {
        background: #e6f2ff !important;
        border-radius: 12px;
        padding: 1rem;
        color: #1a365d !important;
        border-left: 5px solid #667eea;
    }
    
    .stSuccess p {
        color: #1a365d !important;
        font-weight: 600 !important;
    }
    
    .stError {
        background: #fed7d7 !important;
        border-radius: 12px;
        padding: 1rem;
        color: #742a2a !important;
        border-left: 5px solid #e53e3e;
    }
    
    .stError p {
        color: #742a2a !important;
    }
    
    .stWarning {
        background: #feebc8 !important;
        color: #7c2d12 !important;
        border-left: 5px solid #ed8936;
    }
    
    .stWarning p {
        color: #7c2d12 !important;
    }
    
    /* Checkbox */
    .stCheckbox {
        background: #f7fafc;
        padding: 0.5rem;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    .stCheckbox:hover {
        background: #e6f2ff;
    }
    
    .stCheckbox label {
        color: #1a202c !important;
    }
    
    /* Feature card hover effects */
    .feature-card:hover {
        transform: translateY(-10px) scale(1.02) !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Subtitle styling */
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.4rem;
        font-style: italic;
        margin: 1rem 0 0 0;
        font-weight: 400;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Tool cards - Simple and clean */
    .tool-card {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin: 0 0 2rem 0;
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .tool-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        border-left-width: 8px;
    }
    
    .tool-card h2 {
        color: #1a202c !important;
        border: none !important;
        margin-bottom: 0.5rem !important;
        font-size: 2rem !important;
    }
    
    .tool-card p {
        color: #4a5568 !important;
        font-size: 1.1rem;
        margin: 0 !important;
    }
    
    /* Radio buttons - Better spacing and larger text */
    [data-testid="stSidebar"] .stRadio > label {
        color: #ffffff !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        text-align: left !important;
        display: block !important;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: #e2e8f0 !important;
        font-size: 1.2rem !important;
        padding: 1rem 0.5rem !important;
        display: block !important;
        font-weight: 600 !important;
        text-align: left !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        gap: 1.5rem !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label {
        margin-bottom: 1.5rem !important;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] h1 {
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-size: 2rem !important;
        text-align: left !important;
    }
    
    [data-testid="stSidebar"] p {
        color: #e2e8f0 !important;
        font-size: 1.1rem !important;
    }
    

</style>
""", unsafe_allow_html=True)

# Initialize AI client
@st.cache_resource
def get_ai_client():
    return AWSAIClient()

def home_page():
    """Stunning home page"""
    # Hero section with larger text
    st.markdown("""
    <div style='text-align: center; padding: 3.5rem 0 4rem 0;'>
        <h1 style='color: #ffffff; font-size: 5rem; font-weight: 900; margin-bottom: 1.5rem; 
                   text-shadow: 3px 3px 10px rgba(0,0,0,0.4); letter-spacing: -1px;'>
            DevFlow Automator
        </h1>
        <p style='color: #ffffff; font-size: 1.8rem; font-weight: 500; text-shadow: 2px 2px 6px rgba(0,0,0,0.3);'>
            Supercharge your development workflow with AI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards - All 4 in one row
    col1, col2, col3, col4 = st.columns(4, gap="large")
    
    with col1:
        st.markdown("""
        <div class='feature-card' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                    padding: 2.5rem 1.5rem; border-radius: 25px; text-align: center; 
                    box-shadow: 0 15px 40px rgba(250, 112, 154, 0.4); 
                    transform: translateY(0); transition: all 0.4s ease;
                    cursor: pointer; height: 320px; display: flex; flex-direction: column; justify-content: center;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>🤖</div>
            <h3 style='color: white; font-size: 1.5rem; margin-bottom: 0.8rem; font-weight: 900;'>
                AI Commit Messages
            </h3>
            <p style='color: rgba(255,255,255,0.95); font-size: 1rem; line-height: 1.4;'>
                AI-powered commit messages
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🤖 TRY AI COMMIT", key="btn1", use_container_width=True):
            st.session_state.page = "🤖 AI Commit Messages"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class='feature-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 2.5rem 1.5rem; border-radius: 25px; text-align: center; 
                    box-shadow: 0 15px 40px rgba(240, 147, 251, 0.4); 
                    transform: translateY(0); transition: all 0.4s ease;
                    cursor: pointer; height: 320px; display: flex; flex-direction: column; justify-content: center;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>🏷️</div>
            <h3 style='color: white; font-size: 1.5rem; margin-bottom: 0.8rem; font-weight: 900;'>
                Badge Manager
            </h3>
            <p style='color: rgba(255,255,255,0.95); font-size: 1rem; line-height: 1.4;'>
                GitHub badges instantly
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🏷️ MANAGE BADGES", key="btn2", use_container_width=True):
            st.session_state.page = "🏷️ Badge Manager"
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class='feature-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 2.5rem 1.5rem; border-radius: 25px; text-align: center; 
                    box-shadow: 0 15px 40px rgba(79, 172, 254, 0.4); 
                    transform: translateY(0); transition: all 0.4s ease;
                    cursor: pointer; height: 320px; display: flex; flex-direction: column; justify-content: center;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>📚</div>
            <h3 style='color: white; font-size: 1.5rem; margin-bottom: 0.8rem; font-weight: 900;'>
                Project Setup
            </h3>
            <p style='color: rgba(255,255,255,0.95); font-size: 1rem; line-height: 1.4;'>
                Scaffold projects instantly
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📚 SETUP PROJECT", key="btn3", use_container_width=True):
            st.session_state.page = "📚 Project Setup"
            st.rerun()
    
    with col4:
        st.markdown("""
        <div class='feature-card' style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                    padding: 2.5rem 1.5rem; border-radius: 25px; text-align: center; 
                    box-shadow: 0 15px 40px rgba(168, 237, 234, 0.4); 
                    transform: translateY(0); transition: all 0.4s ease;
                    cursor: pointer; height: 320px; display: flex; flex-direction: column; justify-content: center;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>💻</div>
            <h3 style='color: #1a202c; font-size: 1.5rem; margin-bottom: 0.8rem; font-weight: 900;'>
                Code Generator
            </h3>
            <p style='color: #2d3748; font-size: 1rem; line-height: 1.4;'>
                Generate code from descriptions
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💻 GENERATE CODE", key="btn4", use_container_width=True):
            st.session_state.page = "💻 Code Generator"
            st.rerun()

def main():
    # Initialize session state for page navigation
    if 'page' not in st.session_state:
        st.session_state.page = "🏠 Home"
    
    # Sidebar navigation
    st.sidebar.markdown("<h1 style='text-align: left; font-size: 2rem;'>🛠️ Navigation</h1>", unsafe_allow_html=True)
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    
    page = st.sidebar.radio("Choose a page:",
        ["🏠 Home", "🤖 AI Commit Messages", "🏷️ Badge Manager", "📚 Project Setup", "💻 Code Generator"],
        label_visibility="collapsed",
        index=["🏠 Home", "🤖 AI Commit Messages", "🏷️ Badge Manager", "📚 Project Setup", "💻 Code Generator"].index(st.session_state.page) if st.session_state.page in ["🏠 Home", "🤖 AI Commit Messages", "🏷️ Badge Manager", "📚 Project Setup", "💻 Code Generator"] else 0
    )
    
    # Update session state if sidebar selection changes
    if page != st.session_state.page:
        st.session_state.page = page
    
    if st.session_state.page == "🏠 Home":
        home_page()
    elif st.session_state.page == "🤖 AI Commit Messages":
        commit_message_tool()
    elif st.session_state.page == "🏷️ Badge Manager":
        badge_manager_tool()
    elif st.session_state.page == "📚 Project Setup":
        project_setup_tool()
    elif st.session_state.page == "💻 Code Generator":
        code_generator_tool()

def commit_message_tool():
    st.markdown("""
    <div class="tool-card">
        <h2>🤖 AI-Powered Commit Messages</h2>
        <p>Generate meaningful commit messages from your git changes using AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔍 Analyze Current Changes", type="primary", use_container_width=True):
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
                if st.button("✅ Use This Message", use_container_width=True):
                    try:
                        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
                        st.success("🎉 Committed successfully!")
                    except subprocess.CalledProcessError as e:
                        st.error(f"❌ Commit failed: {e}")
            
            with col_b:
                custom_message = st.text_input("Or edit the message:")
                if custom_message and st.button("📝 Commit Custom", use_container_width=True):
                    try:
                        subprocess.run(['git', 'commit', '-m', custom_message], check=True)
                        st.success("🎉 Committed successfully!")
                    except subprocess.CalledProcessError as e:
                        st.error(f"❌ Commit failed: {e}")
                        
        except Exception as e:
            st.error(f"❌ Error: {e}")

def badge_manager_tool():
    st.markdown("""
    <div class="tool-card">
        <h2>🏷️ README Badge Manager</h2>
        <p>Auto-generate and update beautiful README badges for your repository</p>
    </div>
    """, unsafe_allow_html=True)
    
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
            st.subheader("🎯 Select Badges (Choose 2-3 for best results)")
            
            badges = {
                'Stars': f'![Stars](https://img.shields.io/github/stars/{user}/{repo_name}?style=flat-square)',
                'Issues': f'![Issues](https://img.shields.io/github/issues/{user}/{repo_name}?style=flat-square)',
                'License': f'![License](https://img.shields.io/github/license/{user}/{repo_name}?style=flat-square)',
                'Last Commit': f'![Last Commit](https://img.shields.io/github/last-commit/{user}/{repo_name}?style=flat-square)'
            }
            
            selected_badges = []
            col1, col2 = st.columns(2)
            
            for i, (name, markdown) in enumerate(badges.items()):
                col = col1 if i % 2 == 0 else col2
                if col.checkbox(name, value=(name in ['Stars', 'License'])):
                    selected_badges.append(markdown)
            
            if selected_badges:
                st.subheader("🎨 Generated Badge Markdown")
                badge_markdown = ' '.join(selected_badges)
                st.code(badge_markdown, language="markdown")
                
                if st.button("📝 Update README", type="primary", use_container_width=True):
                    update_readme_badges(badge_markdown, user, repo_name)
        else:
            st.error("❌ Could not detect GitHub repository")
            
    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.info("Make sure you're in a git repository with GitHub remote")

def update_readme_badges(badge_markdown, user, repo_name):
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
            action = "Updated"
        else:
            # Add badges at the top after title
            lines = content.split('\n')
            if lines and lines[0].startswith('#'):
                lines.insert(2, badge_section)
                lines.insert(2, '')
                content = '\n'.join(lines)
            else:
                content = badge_section + '\n\n' + content
            action = "Added"
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        st.balloons()
        st.success(f"🎉 {action} badges successfully!")
        st.info(f"💡 Push to GitHub to see live badges: `git add README.md && git commit -m 'Add badges' && git push`")
        st.info(f"🔗 View your repo: https://github.com/{user}/{repo_name}")
        
    except Exception as e:
        st.error(f"❌ Error updating README: {e}")

def project_setup_tool():
    st.markdown("""
    <div class="tool-card">
        <h2>📚 Project Setup Wizard</h2>
        <p>Bootstrap new projects with industry best practices in seconds</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        project_type = st.selectbox(
            "🎯 Choose project type:",
            ["Python Flask", "Python FastAPI", "Node.js Express", "React App"]
        )
    
    with col2:
        project_name = st.text_input("📝 Project name:", placeholder="my-awesome-project")
    
    if st.button("🚀 Create Project", type="primary", use_container_width=True) and project_name:
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
        
        st.balloons()
        st.success(f"🎉 Project '{project_name}' created successfully!")
        st.info(f"📁 Created in: {project_path.absolute()}")
        
        # Show next steps
        st.markdown("<br>", unsafe_allow_html=True)
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

def code_generator_tool():
    st.markdown("""
    <div class="tool-card">
        <h2>💻 AI Code Generator</h2>
        <p>Generate code snippets from natural language descriptions using AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Language selection
    col1, col2 = st.columns(2)
    
    with col1:
        language = st.selectbox(
            "🎯 Programming Language:",
            ["Python", "JavaScript", "TypeScript", "Java", "C++", "Go", "Rust", "SQL", "HTML/CSS"]
        )
    
    with col2:
        code_type = st.selectbox(
            "📝 Code Type:",
            ["Function", "Class", "API Endpoint", "Algorithm", "Database Query", "UI Component", "Utility", "Test"]
        )
    
    # Description input
    description = st.text_area(
        "✍️ Describe what you want to build:",
        placeholder="Example: Create a function that validates email addresses using regex",
        height=150
    )
    
    # Additional context
    with st.expander("⚙️ Advanced Options"):
        include_comments = st.checkbox("Include detailed comments", value=True)
        include_tests = st.checkbox("Generate unit tests", value=False)
        framework = st.text_input("Framework/Library (optional):", placeholder="e.g., Flask, React, Express")
    
    if st.button("🚀 Generate Code", type="primary", use_container_width=True) and description:
        try:
            with st.spinner("🤖 AI is generating your code..."):
                # Build the prompt
                prompt = f"""Generate {language} code for a {code_type.lower()}.

Description: {description}

Requirements:
- Language: {language}
- Type: {code_type}
{"- Framework: " + framework if framework else ""}
{"- Include detailed comments explaining the code" if include_comments else ""}
{"- Include unit tests" if include_tests else ""}

Provide clean, production-ready code following best practices."""

                # Generate code using AI
                ai_client = get_ai_client()
                generated_code = ai_client.generate_code(prompt)
                
                st.success("✅ Code generated successfully!")
                
                # Display generated code
                st.subheader("📄 Generated Code")
                
                # Determine language for syntax highlighting
                lang_map = {
                    "Python": "python",
                    "JavaScript": "javascript",
                    "TypeScript": "typescript",
                    "Java": "java",
                    "C++": "cpp",
                    "Go": "go",
                    "Rust": "rust",
                    "SQL": "sql",
                    "HTML/CSS": "html"
                }
                
                st.code(generated_code, language=lang_map.get(language, "python"))
                
                # Action buttons
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button("📋 Copy to Clipboard", use_container_width=True):
                        st.info("💡 Use Ctrl+C to copy the code above")
                
                with col_b:
                    filename = st.text_input("Save as:", placeholder="code.py")
                    if filename and st.button("💾 Save to File", use_container_width=True):
                        try:
                            with open(filename, 'w', encoding='utf-8') as f:
                                f.write(generated_code)
                            st.success(f"✅ Saved to {filename}")
                        except Exception as e:
                            st.error(f"❌ Error saving file: {e}")
                
                with col_c:
                    if st.button("🔄 Regenerate", use_container_width=True):
                        st.rerun()
                
                # Show explanation
                with st.expander("📚 Code Explanation"):
                    st.markdown("""
                    The generated code follows best practices for **{}** development.
                    
                    **Key Features:**
                    - Clean and readable structure
                    - Proper error handling
                    - Type hints/annotations (where applicable)
                    - Documentation strings
                    {}
                    {}
                    """.format(
                        language,
                        f"- {framework} framework integration" if framework else "",
                        "- Comprehensive unit tests" if include_tests else ""
                    ))
                
        except Exception as e:
            st.error(f"❌ Error generating code: {e}")
            st.info("💡 Try rephrasing your description or check your AWS credentials")

if __name__ == "__main__":
    main()
