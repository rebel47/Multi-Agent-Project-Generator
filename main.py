import argparse
import sys
import traceback
import subprocess
from pathlib import Path

from agent.graph import agent


def run_streamlit_ui():
    """Launch the Streamlit web UI"""
    streamlit_app = Path(__file__).parent / "streamlit_app.py"
    if streamlit_app.exists():
        subprocess.run([sys.executable, "-m", "streamlit", "run", str(streamlit_app)])
    else:
        print("Error: streamlit_app.py not found")
        sys.exit(1)


def run_cli_mode(recursion_limit):
    """Run in CLI mode (interactive)"""
    try:
        user_prompt = input("Enter your project prompt: ")
        project_name = input("Enter a name for this project folder: ").strip()
        if not project_name:
            print("Project name cannot be empty.")
            sys.exit(1)

        # Set up the project root folder
        from agent.tools import set_project_root
        set_project_root(project_name)

        print("\n🚀 Starting project generation...")
        print(f"📦 Project: {project_name}")
        print(f"⚙️  Recursion Limit: {recursion_limit}\n")

        result = agent.invoke(
            {"user_prompt": user_prompt, "project_name": project_name},
            {"recursion_limit": recursion_limit}
        )
        print("✅ Final State:", result)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        traceback.print_exc()
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Multi-Agent Project Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Launch Streamlit web UI
  python main.py --cli              # Run in CLI mode
  python main.py --cli -r 150       # CLI mode with custom recursion limit
        """
    )
    parser.add_argument("--ui", "--streamlit", action="store_true", 
                        help="Launch Streamlit web UI (default)")
    parser.add_argument("--cli", action="store_true", 
                        help="Run in CLI mode (interactive)")
    parser.add_argument("--recursion-limit", "-r", type=int, default=100,
                        help="Recursion limit for processing (default: 100)")

    args = parser.parse_args()

    # Determine mode
    if args.cli:
        run_cli_mode(args.recursion_limit)
    else:
        # Default to UI mode
        run_streamlit_ui()


if __name__ == "__main__":
    main()