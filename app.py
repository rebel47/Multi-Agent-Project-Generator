"""
Gradio Web UI for Multi-Agent Project Generator
"""
import gradio as gr
from pathlib import Path
import json
from datetime import datetime
from agent.graph_enhanced import agent
from agent.config import app_config, ApplicationConfig, ModelProvider
from agent.tools_enhanced import set_project_root
from agent.logger import logger
from templates import list_templates, get_template_info, get_template


def generate_project_from_prompt(
    prompt: str,
    project_name: str,
    use_template: bool,
    template_name: str,
    enable_review: bool,
    enable_testing: bool,
    enable_git: bool,
    enable_docker: bool,
    provider: str,
    model_name: str,
    recursion_limit: int
):
    """Generate a project from prompt or template."""
    try:
        if not project_name:
            return "❌ Error: Project name is required", ""
        
        if not prompt and not use_template:
            return "❌ Error: Either provide a prompt or select a template", ""
        
        # Update config
        app_config.enable_code_review = enable_review
        app_config.enable_testing = enable_testing
        app_config.enable_git = enable_git
        app_config.enable_docker = enable_docker
        app_config.max_recursion_limit = recursion_limit
        
        # Update model provider
        provider_enum = ModelProvider(provider.lower())
        app_config.agent_config.planner_model.provider = provider_enum
        app_config.agent_config.architect_model.provider = provider_enum
        app_config.agent_config.coder_model.provider = provider_enum
        
        if model_name:
            app_config.agent_config.planner_model.model_name = model_name
            app_config.agent_config.architect_model.model_name = model_name
            app_config.agent_config.coder_model.model_name = model_name
        
        # Use template if selected
        final_prompt = prompt
        if use_template and template_name:
            template = get_template(template_name)
            if template:
                final_prompt = f"""Create a {template.name} with the following specifications:
                
Description: {template.description}
Tech Stack: {template.techstack}
Features: {', '.join(template.features)}

User additional requirements: {prompt if prompt else 'None'}
"""
        
        # Set project root
        set_project_root(project_name)
        
        # Generate project
        logger.info(f"🚀 Starting project generation: {project_name}")
        
        result = agent.invoke(
            {
                "user_prompt": final_prompt,
                "project_name": project_name
            },
            {"recursion_limit": recursion_limit}
        )
        
        metadata = result.get("metadata")
        status = result.get("status")
        
        # Build result summary
        summary = f"""
## ✅ Project Generated Successfully!

**Project Name:** {project_name}
**Status:** {status}
**Files Created:** {len(metadata.files_created) if metadata else 'Unknown'}
**Git Initialized:** {'Yes' if metadata and metadata.git_initialized else 'No'}
**Tests Generated:** {'Yes' if metadata and metadata.tests_generated else 'No'}
**Docker Enabled:** {'Yes' if metadata and metadata.docker_enabled else 'No'}

**Location:** `generated_project/{project_name}/`

### Files Created:
{chr(10).join(f'- {file}' for file in (metadata.files_created[:20] if metadata else []))}
{f'... and {len(metadata.files_created) - 20} more files' if metadata and len(metadata.files_created) > 20 else ''}

### Next Steps:
1. Navigate to the project directory
2. Review the generated code
3. Install dependencies (check requirements.txt or package.json)
4. Run the project!
"""
        
        # Get file tree
        project_path = Path("generated_project") / project_name
        file_tree = get_directory_tree(project_path)
        
        return summary, file_tree
        
    except Exception as e:
        logger.error(f"Error generating project: {str(e)}")
        return f"❌ Error: {str(e)}", ""


def get_directory_tree(path: Path, prefix: str = "", max_depth: int = 3, current_depth: int = 0) -> str:
    """Generate a visual directory tree."""
    if current_depth >= max_depth:
        return ""
    
    if not path.exists():
        return "Directory not found"
    
    tree = []
    try:
        items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            current_prefix = "└── " if is_last else "├── "
            tree.append(f"{prefix}{current_prefix}{item.name}")
            
            if item.is_dir() and not item.name.startswith('.'):
                extension = "    " if is_last else "│   "
                subtree = get_directory_tree(item, prefix + extension, max_depth, current_depth + 1)
                if subtree:
                    tree.append(subtree)
    except PermissionError:
        pass
    
    return "\n".join(tree)


def get_template_details(template_name: str):
    """Get detailed information about a template."""
    if not template_name:
        return "Select a template to see details"
    
    info = get_template_info(template_name)
    if not info:
        return "Template not found"
    
    return f"""
### {info['name']}

**Description:** {info['description']}

**Tech Stack:** {info['techstack']}

**Features:**
{chr(10).join(f'- {feature}' for feature in info['features'])}

**Files:** {info['file_count']} files will be generated
"""


def list_generated_projects():
    """List all generated projects."""
    projects_dir = Path("generated_project")
    if not projects_dir.exists():
        return "No projects generated yet"
    
    projects = [p.name for p in projects_dir.iterdir() if p.is_dir()]
    if not projects:
        return "No projects generated yet"
    
    return "\n".join(f"- {project}" for project in projects)


def view_project_file(project_name: str, filename: str):
    """View contents of a generated file."""
    if not project_name or not filename:
        return "Select a project and file"
    
    try:
        file_path = Path("generated_project") / project_name / filename
        if not file_path.exists():
            return "File not found"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"


# Build Gradio Interface
with gr.Blocks(title="Multi-Agent Project Generator") as app:
    gr.Markdown("""
    # 🤖 Multi-Agent Project Generator
    
    Generate complete, production-ready projects using AI agents!
    """)
    
    with gr.Tabs():
        # Tab 1: Generate Project
        with gr.Tab("🚀 Generate Project"):
            with gr.Row():
                with gr.Column(scale=2):
                    prompt_input = gr.Textbox(
                        label="Project Description",
                        placeholder="Describe the project you want to build...",
                        lines=5
                    )
                    project_name_input = gr.Textbox(
                        label="Project Name",
                        placeholder="my-awesome-project"
                    )
                    
                    with gr.Accordion("📋 Use Template (Optional)", open=False):
                        use_template_checkbox = gr.Checkbox(label="Use Template")
                        template_dropdown = gr.Dropdown(
                            choices=list_templates(),
                            label="Select Template"
                        )
                        template_details = gr.Markdown("Select a template to see details")
                        template_dropdown.change(
                            get_template_details,
                            inputs=[template_dropdown],
                            outputs=[template_details]
                        )
                    
                    with gr.Accordion("⚙️ Advanced Settings", open=False):
                        with gr.Row():
                            enable_review = gr.Checkbox(label="Code Review", value=True)
                            enable_testing = gr.Checkbox(label="Generate Tests", value=True)
                            enable_git = gr.Checkbox(label="Git Init", value=True)
                            enable_docker = gr.Checkbox(label="Docker Config", value=False)
                        
                        provider_dropdown = gr.Dropdown(
                            choices=["gemini", "openai", "anthropic", "groq"],
                            label="LLM Provider",
                            value="gemini"
                        )
                        model_input = gr.Textbox(
                            label="Model Name",
                            value="gemini-2.0-flash-exp",
                            placeholder="e.g., gpt-4, claude-3-opus"
                        )
                        recursion_slider = gr.Slider(
                            minimum=50,
                            maximum=200,
                            value=100,
                            step=10,
                            label="Recursion Limit"
                        )
                    
                    generate_btn = gr.Button("🚀 Generate Project", variant="primary", size="lg")
                
                with gr.Column(scale=1):
                    gr.Markdown("### 📊 Generation Status")
                    output_status = gr.Markdown("Ready to generate...")
                    output_tree = gr.Code(label="Project Structure", language="shell")
        
        # Tab 2: Browse Projects
        with gr.Tab("📁 Browse Projects"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### Generated Projects")
                    refresh_btn = gr.Button("🔄 Refresh")
                    projects_list = gr.Markdown(list_generated_projects())
                    refresh_btn.click(list_generated_projects, outputs=[projects_list])
                
                with gr.Column(scale=2):
                    project_selector = gr.Textbox(label="Project Name")
                    file_selector = gr.Textbox(label="File Path")
                    view_btn = gr.Button("👁️ View File")
                    file_content = gr.Code(label="File Content", language="python")
                    view_btn.click(
                        view_project_file,
                        inputs=[project_selector, file_selector],
                        outputs=[file_content]
                    )
        
        # Tab 3: Documentation
        with gr.Tab("📚 Documentation"):
            gr.Markdown("""
            ## How to Use
            
            ### 1. Generate from Prompt
            - Enter a description of what you want to build
            - Give your project a name
            - Configure settings
            - Click "Generate Project"
            
            ### 2. Use a Template
            - Check "Use Template"
            - Select a template from the dropdown
            - Optionally add custom requirements
            - Generate!
            
            ### 3. Advanced Settings
            - **Code Review**: Enable automated code review
            - **Generate Tests**: Create unit tests automatically
            - **Git Init**: Initialize git repository
            - **Docker Config**: Generate Docker files
            - **LLM Provider**: Choose your AI provider
            - **Recursion Limit**: Adjust for complex projects
            
            ### Available Templates
            
            - **FastAPI REST API**: Modern Python API
            - **React SPA**: Single-page React application
            - **Django Web App**: Full-featured Django project
            - **Flask Microservice**: Lightweight Flask service
            - **Next.js Full-Stack**: Modern full-stack app
            - **Python CLI Tool**: Command-line interface
            - **Data Pipeline**: ETL data processing
            
            ### Requirements
            
            Make sure you have set up your API keys in the `.env` file:
            ```
            GEMINI_API_KEY=your_key_here
            OPENAI_API_KEY=your_key_here  # if using OpenAI
            ANTHROPIC_API_KEY=your_key_here  # if using Anthropic
            ```
            
            ### Output Location
            
            Generated projects are saved in: `generated_project/<project-name>/`
            """)
    
    # Connect generate button
    generate_btn.click(
        generate_project_from_prompt,
        inputs=[
            prompt_input,
            project_name_input,
            use_template_checkbox,
            template_dropdown,
            enable_review,
            enable_testing,
            enable_git,
            enable_docker,
            provider_dropdown,
            model_input,
            recursion_slider
        ],
        outputs=[output_status, output_tree]
    )


def launch_ui(share=False, server_port=7860):
    """Launch the Gradio interface."""
    logger.info(f"🌐 Launching Gradio UI on port {server_port}")
    try:
        app.launch(share=share, server_port=server_port)
    except Exception as e:
        logger.error(f"Failed to launch UI: {e}")
        # Fallback without theme if it causes issues
        app.launch(share=share, server_port=server_port)


if __name__ == "__main__":
    launch_ui(share=False)
