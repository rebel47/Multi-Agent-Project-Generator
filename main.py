import argparse
import sys
import traceback

from agent.graph import agent


def main():
    parser = argparse.ArgumentParser(description="Run engineering project planner")
    parser.add_argument("--recursion-limit", "-r", type=int, default=100,
                        help="Recursion limit for processing (default: 100)")

    args = parser.parse_args()

    try:
        user_prompt = input("Enter your project prompt: ")
        project_name = input("Enter a name for this project folder: ").strip()
        if not project_name:
            print("Project name cannot be empty.")
            sys.exit(1)

        # Set up the project root folder
        from agent.tools import set_project_root
        set_project_root(project_name)

        result = agent.invoke(
            {"user_prompt": user_prompt, "project_name": project_name},
            {"recursion_limit": args.recursion_limit}
        )
        print("Final State:", result)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        traceback.print_exc()
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()