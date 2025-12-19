import argparse
import sys
import traceback
from pathlib import Path

from agent.graph_enhanced import agent
from agent.config import app_config, ModelProvider
from agent.logger import logger, AgentProgress
from agent.tools_enhanced import set_project_root
from templates import list_templates, get_template, get_template_info


def main():
    parser = argparse.ArgumentParser(
        description="Multi-Agent Project Generator - Generate complete projects with AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate from prompt
  python main.py --prompt "Build a REST API" --name my-api
  
  # Use a template
  python main.py --template fastapi-rest-api --name my-api
  
  # List available templates
  python main.py --list-templates
  
  # Enable all features
  python main.py --prompt "Todo app" --name todo --review --test --git --docker
  
  # Use different model provider
  python main.py --prompt "CLI tool" --name cli --provider openai --model gpt-4
        """
    )
    
    # Project specification
    parser.add_argument("--prompt", "-p", type=str, help="Project description prompt")
    parser.add_argument("--name", "-n", type=str, help="Project name")
    parser.add_argument("--template", "-t", type=str, choices=list_templates(), 
                       help="Use a project template")
    parser.add_argument("--list-templates", "-l", action="store_true",
                       help="List available templates")
    
    # Features
    parser.add_argument("--review", action="store_true", default=True,
                       help="Enable code review (default: True)")
    parser.add_argument("--no-review", action="store_true",
                       help="Disable code review")
    parser.add_argument("--test", action="store_true", default=True,
                       help="Generate tests (default: True)")
    parser.add_argument("--no-test", action="store_true",
                       help="Skip test generation")
    parser.add_argument("--git", action="store_true", default=True,
                       help="Initialize git repository (default: True)")
    parser.add_argument("--no-git", action="store_true",
                       help="Skip git initialization")
    parser.add_argument("--docker", action="store_true", default=False,
                       help="Generate Docker configuration")
    parser.add_argument("--web-search", action="store_true", default=False,
                       help="Enable web search capability")
    
    # Model configuration
    parser.add_argument("--provider", type=str, default="gemini",
                       choices=["gemini", "openai", "anthropic", "groq"],
                       help="LLM provider (default: gemini)")
    parser.add_argument("--model", type=str,
                       help="Model name (e.g., gemini-2.0-flash-exp, gpt-4, claude-3-opus)")
    parser.add_argument("--recursion-limit", "-r", type=int, default=100,
                       help="Recursion limit for processing (default: 100)")
    
    # UI options
    parser.add_argument("--ui", action="store_true",
                       help="Launch web UI instead of CLI")
    parser.add_argument("--port", type=int, default=7860,
                       help="Port for web UI (default: 7860)")
    parser.add_argument("--share", action="store_true",
                       help="Create public share link for web UI")

    args = parser.parse_args()

    # List templates if requested
    if args.list_templates:
        print("\n📋 Available Project Templates:\n")
        for template_name in list_templates():
            info = get_template_info(template_name)
            print(f"  • {template_name}")
            print(f"    {info['description']}")
            print(f"    Tech: {info['techstack']}")
            print()
        return

    # Launch web UI if requested
    if args.ui:
        from app import launch_ui
        launch_ui(share=args.share, server_port=args.port)
        return

    try:
        # Get project prompt and name
        if args.template:
            template = get_template(args.template)
            if not template:
                print(f"❌ Template '{args.template}' not found")
                sys.exit(1)
            
            user_prompt = f"""Create a {template.name} with the following specifications:
            
Description: {template.description}
Tech Stack: {template.techstack}
Features: {', '.join(template.features)}
"""
            if args.prompt:
                user_prompt += f"\n\nAdditional requirements: {args.prompt}"
            
            print(f"\n🎯 Using template: {template.name}")
        else:
            user_prompt = args.prompt if args.prompt else input("Enter your project prompt: ")
        
        project_name = args.name if args.name else input("Enter a name for this project folder: ").strip()
        
        if not project_name:
            print("❌ Project name cannot be empty.")
            sys.exit(1)

        # Configure application
        app_config.enable_code_review = args.review and not args.no_review
        app_config.enable_testing = args.test and not args.no_test
        app_config.enable_git = args.git and not args.no_git
        app_config.enable_docker = args.docker
        app_config.enable_web_search = args.web_search
        app_config.max_recursion_limit = args.recursion_limit
        
        # Configure model provider
        provider = ModelProvider(args.provider.lower())
        app_config.agent_config.planner_model.provider = provider
        app_config.agent_config.architect_model.provider = provider
        app_config.agent_config.coder_model.provider = provider
        app_config.agent_config.reviewer_model.provider = provider
        app_config.agent_config.tester_model.provider = provider
        
        if args.model:
            app_config.agent_config.planner_model.model_name = args.model
            app_config.agent_config.architect_model.model_name = args.model
            app_config.agent_config.coder_model.model_name = args.model
            app_config.agent_config.reviewer_model.model_name = args.model
            app_config.agent_config.tester_model.model_name = args.model
        
        # Set up the project root folder
        set_project_root(project_name)
        
        # Display configuration
        print(f"\n⚙️  Configuration:")
        print(f"   Provider: {args.provider}")
        print(f"   Model: {args.model or 'default'}")
        print(f"   Code Review: {'✅' if app_config.enable_code_review else '❌'}")
        print(f"   Testing: {'✅' if app_config.enable_testing else '❌'}")
        print(f"   Git: {'✅' if app_config.enable_git else '❌'}")
        print(f"   Docker: {'✅' if app_config.enable_docker else '❌'}")
        print(f"   Recursion Limit: {args.recursion_limit}")
        print()
        
        logger.info(f"🚀 Starting project generation: {project_name}")
        
        # Generate project
        with AgentProgress() as progress:
            result = agent.invoke(
                {"user_prompt": user_prompt, "project_name": project_name},
                {"recursion_limit": args.recursion_limit}
            )
        
        # Display results
        print("\n" + "="*60)
        print("🎉 PROJECT GENERATION COMPLETE!")
        print("="*60)
        
        metadata = result.get("metadata")
        if metadata:
            print(f"\n📊 Project Summary:")
            print(f"   Name: {metadata.project_name}")
            print(f"   Files Created: {len(metadata.files_created)}")
            print(f"   Git Initialized: {'Yes' if metadata.git_initialized else 'No'}")
            print(f"   Tests Generated: {'Yes' if metadata.tests_generated else 'No'}")
            print(f"   Docker Enabled: {'Yes' if metadata.docker_enabled else 'No'}")
            print(f"\n📁 Location: generated_project/{project_name}/")
        
        print("\n✅ Your project is ready!")
        print(f"\nNext steps:")
        print(f"  1. cd generated_project/{project_name}")
        print(f"  2. Review the generated code")
        print(f"  3. Install dependencies (check requirements.txt or package.json)")
        print(f"  4. Run your project!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        traceback.print_exc()
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()