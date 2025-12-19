"""
Streamlit Web UI for Multi-Agent Project Generator
Improved version with project results viewer
"""
import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
import json
from datetime import datetime
import sys

# Configure Streamlit
st.set_page_config(
    page_title="Multi-Agent Project Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Suppress debug/verbose logging
import logging
logging.getLogger("langchain").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)

try:
    from agent.graph import agent
    from agent.tools import set_project_root, list_files, read_file
except ImportError as e:
    st.error(f"Failed to import agent modules: {e}")
    st.stop()

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'projects' not in st.session_state:
        st.session_state.projects = []
    if 'current_project' not in st.session_state:
        st.session_state.current_project = None
    if 'generation_status' not in st.session_state:
        st.session_state.generation_status = None


def get_projects():
    """Get list of generated projects"""
    projects_dir = Path("generated_project")
    if not projects_dir.exists():
        return []
    
    projects = []
    for project_dir in projects_dir.iterdir():
        if project_dir.is_dir():
            files = list(project_dir.rglob('*'))
            file_count = len([f for f in files if f.is_file()])
            projects.append({
                'name': project_dir.name,
                'path': str(project_dir),
                'files': file_count,
                'created': datetime.fromtimestamp(project_dir.stat().st_ctime)
            })
    
    return sorted(projects, key=lambda x: x['created'], reverse=True)


def render_project_tree(path, prefix="", max_depth=3, current_depth=0):
    """Render project file tree"""
    if current_depth >= max_depth:
        return []
    
    items = []
    try:
        entries = sorted(Path(path).iterdir(), key=lambda x: (not x.is_dir(), x.name))
        for entry in entries:
            if entry.name.startswith('.'):
                continue
            
            indent = "  " * current_depth
            if entry.is_dir():
                items.append(f"{indent}📁 {entry.name}/")
                if current_depth < max_depth - 1:
                    items.extend(render_project_tree(entry, prefix, max_depth, current_depth + 1))
            else:
                icon = "📄"
                if entry.suffix in ['.py', '.js', '.ts', '.jsx', '.tsx']:
                    icon = "💻"
                elif entry.suffix in ['.json', '.yaml', '.yml']:
                    icon = "⚙️"
                elif entry.suffix in ['.md', '.txt']:
                    icon = "📝"
                items.append(f"{indent}{icon} {entry.name}")
    except PermissionError:
        pass
    
    return items


def view_file_content(project_path, file_path):
    """View file content"""
    full_path = Path(project_path) / file_path
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"


def generate_project(prompt, project_name, provider, recursion_limit):
    """Generate a new project"""
    try:
        set_project_root(project_name)
        
        with st.spinner(f"🚀 Generating project '{project_name}'..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text(f"⏳ Starting generation... Using {provider} provider")
            progress_bar.progress(10)
            
            status_text.text("📋 Planning project structure...")
            progress_bar.progress(20)
            
            status_text.text("🏗️ Architecting implementation...")
            progress_bar.progress(40)
            
            status_text.text("💻 Generating code...")
            progress_bar.progress(60)
            
            result = agent.invoke(
                {"user_prompt": prompt, "project_name": project_name},
                {"recursion_limit": recursion_limit}
            )
            
            status_text.text("✅ Project generated successfully!")
            progress_bar.progress(100)
            
            return result
    except Exception as e:
        st.error(f"❌ Error generating project: {str(e)}")
        return None


# Main App
def main():
    initialize_session_state()
    
    # Header
    st.markdown("# 🤖 Multi-Agent Project Generator")
    st.markdown("Generate complete projects with AI agents powered by OpenAI & Gemini")
    
    # Main Navigation
    tab1, tab2, tab3 = st.tabs(["🚀 Generate", "📂 Browse Projects", "📚 About"])
    
    # ============ TAB 1: GENERATE ============
    with tab1:
        st.markdown("## Generate a New Project")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Project Details
            st.subheader("📋 Project Details")
            
            project_name = st.text_input(
                "Project Name",
                placeholder="e.g., my-awesome-app",
                help="Name for your project folder"
            )
            
            project_prompt = st.text_area(
                "Project Description",
                placeholder="Describe what you want to build. Be specific!",
                height=150,
                help="Detailed description helps generate better code"
            )
            
            # Configuration
            st.subheader("⚙️ Configuration")
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                provider = st.selectbox(
                    "LLM Provider",
                    ["openai", "gemini"],
                    help="Choose your AI provider"
                )
            
            with col_b:
                if provider == "openai":
                    model = st.selectbox(
                        "Model",
                        ["gpt-4", "gpt-3.5-turbo"],
                        help="Select model"
                    )
                else:
                    model = st.selectbox(
                        "Model",
                        ["gemini-pro", "gemini-2.0-flash"],
                        help="Select model"
                    )
            
            with col_c:
                recursion_limit = st.slider(
                    "Recursion Limit",
                    min_value=50,
                    max_value=200,
                    value=100,
                    step=10,
                    help="Higher = more iterations"
                )
            
            # Generate Button
            if st.button("🚀 Generate Project", use_container_width=True, type="primary"):
                if not project_name:
                    st.error("❌ Please enter a project name")
                elif not project_prompt:
                    st.error("❌ Please describe your project")
                else:
                    st.session_state.generation_status = generate_project(
                        project_prompt,
                        project_name,
                        provider,
                        recursion_limit
                    )
                    
                    if st.session_state.generation_status:
                        st.success(f"✅ Project '{project_name}' generated successfully!")
                        st.balloons()
        
        with col2:
            st.subheader("💡 Tips")
            st.info("""
            **Good Prompts:**
            - "Build a REST API with FastAPI and PostgreSQL for managing tasks"
            - "Create a React dashboard with real-time charts"
            - "Python CLI tool for batch image processing"
            
            **Use descriptive language:**
            - Mention tech preferences
            - Describe key features
            - Specify requirements
            """)
        
        # Generation Result
        if st.session_state.generation_status:
            st.divider()
            st.subheader("📊 Generation Result")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Status", "✅ Complete")
            with col2:
                st.metric("Project", project_name)
            with col3:
                st.metric("Provider", provider.upper())
    
    # ============ TAB 2: BROWSE PROJECTS ============
    with tab2:
        st.markdown("## Browse Generated Projects")
        
        projects = get_projects()
        
        if not projects:
            st.info("📭 No projects generated yet. Generate one in the 'Generate' tab!")
        else:
            # Projects List
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.subheader("📂 Projects")
                selected_project = st.selectbox(
                    "Select a project",
                    options=[p['name'] for p in projects],
                    format_func=lambda x: f"📦 {x}",
                    label_visibility="collapsed"
                )
                
                # Project Info
                if selected_project:
                    project = next((p for p in projects if p['name'] == selected_project), None)
                    if project:
                        st.metric("Files", project['files'])
                        st.metric("Created", project['created'].strftime("%Y-%m-%d %H:%M"))
            
            with col2:
                if selected_project:
                    project = next((p for p in projects if p['name'] == selected_project), None)
                    
                    # Tabs for project view
                    sub_tab1, sub_tab2, sub_tab3 = st.tabs(["📂 Structure", "📝 Files", "📊 Stats"])
                    
                    with sub_tab1:
                        st.subheader("Project Structure")
                        tree_items = render_project_tree(project['path'])
                        if tree_items:
                            tree_text = "\n".join(tree_items)
                            st.code(tree_text, language="")
                        else:
                            st.info("Empty project directory")
                    
                    with sub_tab2:
                        st.subheader("View Files")
                        
                        # Get all files
                        all_files = []
                        for file_path in Path(project['path']).rglob('*'):
                            if file_path.is_file() and not str(file_path).startswith('.'):
                                rel_path = file_path.relative_to(project['path'])
                                all_files.append(str(rel_path))
                        
                        all_files.sort()
                        
                        if all_files:
                            selected_file = st.selectbox(
                                "Select file to view",
                                options=all_files,
                                format_func=lambda x: f"📄 {x}"
                            )
                            
                            if selected_file:
                                content = view_file_content(project['path'], selected_file)
                                
                                # Determine language
                                ext = Path(selected_file).suffix
                                lang_map = {
                                    '.py': 'python',
                                    '.js': 'javascript',
                                    '.jsx': 'javascript',
                                    '.ts': 'typescript',
                                    '.tsx': 'typescript',
                                    '.json': 'json',
                                    '.yaml': 'yaml',
                                    '.yml': 'yaml',
                                    '.md': 'markdown',
                                    '.html': 'html',
                                    '.css': 'css'
                                }
                                lang = lang_map.get(ext, 'text')
                                
                                st.code(content, language=lang)
                                
                                # Download button
                                st.download_button(
                                    "⬇️ Download File",
                                    content,
                                    file_name=selected_file,
                                    mime="text/plain"
                                )
                        else:
                            st.info("No files in this project")
                    
                    with sub_tab3:
                        st.subheader("Project Statistics")
                        
                        # Calculate stats
                        total_files = 0
                        total_lines = 0
                        file_types = {}
                        
                        for file_path in Path(project['path']).rglob('*'):
                            if file_path.is_file():
                                total_files += 1
                                ext = file_path.suffix or 'other'
                                file_types[ext] = file_types.get(ext, 0) + 1
                                
                                try:
                                    with open(file_path, 'r', encoding='utf-8') as f:
                                        total_lines += len(f.readlines())
                                except:
                                    pass
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Files", total_files)
                        with col2:
                            st.metric("Total Lines", total_lines)
                        with col3:
                            st.metric("File Types", len(file_types))
                        
                        # File type breakdown
                        if file_types:
                            st.bar_chart(file_types)
    
    # ============ TAB 3: ABOUT ============
    with tab3:
        st.markdown("""
        ## About Multi-Agent Project Generator
        
        ### 🎯 What is it?
        An intelligent system that generates complete, production-ready projects using AI agents.
        
        ### 🤖 Powered By
        - **OpenAI GPT-4**: Advanced code generation
        - **Google Gemini**: Fast, free alternative
        - **LangGraph**: Agent orchestration
        - **LangChain**: LLM integration
        
        ### ✨ Features
        - 🚀 Generate projects from natural language
        - 📂 Browse and view generated files
        - 💻 Multiple programming languages
        - 🔄 Iterative generation
        - 📊 Project statistics
        
        ### 🛠️ Technology Stack
        - Python 3.9+
        - Streamlit (UI)
        - LangChain & LangGraph (AI)
        - OpenAI & Gemini APIs
        
        ### 📖 How to Use
        1. Go to the **Generate** tab
        2. Describe your project
        3. Click "Generate Project"
        4. View results in **Browse Projects**
        
        ### 🔗 Links
        - [GitHub Repository](https://github.com/rebel47/Multi-Agent-Project-Generator)
        - [Documentation](https://github.com/rebel47/Multi-Agent-Project-Generator/blob/main/README.md)
        
        ---
        Made with ❤️ for developers
        """)


if __name__ == "__main__":
    main()
