"""
Enhanced multi-agent graph with code review, testing, and advanced features.
"""
from datetime import datetime
from pathlib import Path
from typing import Annotated
from dotenv import load_dotenv
try:
    from langchain.globals import set_verbose, set_debug
except ImportError:
    # Fallback for newer langchain versions
    def set_verbose(val): pass
    def set_debug(val): pass
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent

from agent.prompts import *
from agent.states import *
from agent.config import app_config, get_llm_from_config
from agent.logger import (
    logger, log_agent_start, log_agent_complete, log_agent_error,
    AgentProgress, token_tracker, log_project_summary
)

# Import enhanced tools
from agent.tools_enhanced import (
    write_file, read_file, get_current_directory, list_files,
    git_init, git_commit, git_status,
    generate_requirements_txt, generate_package_json,
    web_search, generate_dockerfile, generate_docker_compose,
    generate_github_actions_workflow
)

_ = load_dotenv()

# Configure debugging based on config
set_debug(app_config.enable_debug)
set_verbose(app_config.enable_verbose)

# Initialize LLMs lazily (only when needed)
def get_planner_llm():
    return get_llm_from_config(app_config.agent_config.planner_model)

def get_architect_llm():
    return get_llm_from_config(app_config.agent_config.architect_model)

def get_coder_llm():
    return get_llm_from_config(app_config.agent_config.coder_model)

def get_reviewer_llm():
    return get_llm_from_config(app_config.agent_config.reviewer_model)

def get_tester_llm():
    return get_llm_from_config(app_config.agent_config.tester_model)


def planner_agent(state: dict) -> dict:
    """Converts user prompt into a structured Plan."""
    log_agent_start("Planner", state)
    
    try:
        user_prompt = state["user_prompt"]
        planner_llm = get_planner_llm()
        resp = planner_llm.with_structured_output(Plan).invoke(
            planner_prompt(user_prompt)
        )
        if resp is None:
            raise ValueError("Planner did not return a valid response.")
        
        logger.info(f"📋 Plan created: {resp.name}")
        logger.info(f"Tech stack: {resp.techstack}")
        logger.info(f"Files to create: {len(resp.files)}")
        
        log_agent_complete("Planner", resp)
        return {
            "plan": resp,
            "project_name": state.get("project_name"),
            "metadata": ProjectMetadata(
                project_name=state.get("project_name", "unknown"),
                created_at=datetime.now().isoformat()
            )
        }
    except Exception as e:
        log_agent_error("Planner", e)
        raise


def architect_agent(state: dict) -> dict:
    """Creates TaskPlan from Plan."""
    log_agent_start("Architect", state)
    
    try:
        plan: Plan = state["plan"]
        architect_llm = get_architect_llm()
        resp = architect_llm.with_structured_output(TaskPlan).invoke(
            architect_prompt(plan=plan.model_dump_json())
        )
        if resp is None:
            raise ValueError("Architect did not return a valid response.")

        resp.plan = plan
        logger.info(f"🏗️ Task plan created with {len(resp.implementation_steps)} steps")
        
        log_agent_complete("Architect", resp)
        return {
            "task_plan": resp,
            "plan": plan,
            "project_name": state.get("project_name"),
            "metadata": state.get("metadata")
        }
    except Exception as e:
        log_agent_error("Architect", e)
        raise


def coder_agent(state: dict) -> dict:
    """LangGraph tool-using coder agent with enhanced capabilities."""
    coder_state: CoderState = state.get("coder_state")
    if coder_state is None:
        log_agent_start("Coder", state)
        coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)

    steps = coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        logger.success("✅ All coding tasks completed")
        return {
            "coder_state": coder_state,
            "status": "CODING_DONE",
            "project_name": state.get("project_name"),
            "plan": state.get("plan"),
            "metadata": state.get("metadata")
        }

    current_task = steps[coder_state.current_step_idx]
    project_name = state.get("project_name")
    
    logger.info(f"💻 [{coder_state.current_step_idx + 1}/{len(steps)}] Working on: {current_task.filepath}")
    
    try:
        existing_content = read_file.run(current_task.filepath, project_name=project_name)

        system_prompt = coder_system_prompt()
        user_prompt = (
            f"Task #{coder_state.current_step_idx + 1}: {current_task.task_description}\n"
            f"File: {current_task.filepath}\n"
            f"Priority: {current_task.priority}\n"
            f"Complexity: {current_task.estimated_complexity}\n"
            f"Existing content:\n{existing_content}\n\n"
            "Use write_file(path, content) to save your changes.\n"
            "You can use other tools as needed (git, package management, etc.)."
        )

        coder_tools = [
            read_file, write_file, list_files, get_current_directory,
            git_commit, git_status, generate_requirements_txt, generate_package_json
        ]
        
        if app_config.enable_web_search:
            coder_tools.append(web_search)
        
        coder_llm = get_coder_llm()
        react_agent = create_react_agent(coder_llm, coder_tools)
        react_agent.invoke({
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        })

        coder_state.current_step_idx += 1
        
        return {
            "coder_state": coder_state,
            "project_name": project_name,
            "plan": state.get("plan"),
            "metadata": state.get("metadata")
        }
    except Exception as e:
        log_agent_error("Coder", e)
        logger.warning(f"Skipping task due to error, moving to next...")
        coder_state.current_step_idx += 1
        return {
            "coder_state": coder_state,
            "project_name": project_name,
            "plan": state.get("plan"),
            "metadata": state.get("metadata")
        }


def reviewer_agent(state: dict) -> dict:
    """Reviews generated code for quality and issues."""
    if not app_config.enable_code_review:
        logger.info("⏭️  Code review disabled, skipping...")
        return {
            **state,
            "status": "REVIEW_DONE",
            "review_results": []
        }
    
    log_agent_start("Reviewer", state)
    
    try:
        project_name = state.get("project_name")
        plan: Plan = state.get("plan")
        review_results = []
        
        # Review each file
        for file in plan.files:
            logger.info(f"🔍 Reviewing: {file.path}")
            
            try:
                code = read_file.run(file.path, project_name=project_name)
                if not code or "ERROR" in code:
                    continue
                
                # Determine language from file extension
                ext = Path(file.path).suffix
                language_map = {
                    ".py": "python", ".js": "javascript", ".jsx": "javascript",
                    ".ts": "typescript", ".tsx": "typescript", ".java": "java",
                    ".go": "go", ".rs": "rust", ".cpp": "c++", ".c": "c"
                }
                language = language_map.get(ext, "unknown")
                
                reviewer_llm = get_reviewer_llm()
                review_response = reviewer_llm.with_structured_output(CodeReviewResult).invoke(
                    reviewer_prompt(file.path, code, language)
                )
                
                review_results.append(review_response)
                
                if review_response.approved:
                    logger.success(f"✅ {file.path} approved (score: {review_response.quality_score})")
                else:
                    logger.warning(f"⚠️  {file.path} needs improvement (score: {review_response.quality_score})")
                    logger.warning(f"Issues: {', '.join(review_response.issues[:3])}")
                    
            except Exception as e:
                logger.error(f"Error reviewing {file.path}: {str(e)}")
        
        log_agent_complete("Reviewer", {"reviews": len(review_results)})
        
        return {
            **state,
            "status": "REVIEW_DONE",
            "review_results": review_results
        }
    except Exception as e:
        log_agent_error("Reviewer", e)
        return {**state, "status": "REVIEW_DONE", "review_results": []}


def tester_agent(state: dict) -> dict:
    """Generates unit tests for the code."""
    if not app_config.enable_testing:
        logger.info("⏭️  Testing disabled, skipping...")
        return {**state, "status": "TEST_DONE", "test_plans": []}
    
    log_agent_start("Tester", state)
    
    try:
        project_name = state.get("project_name")
        plan: Plan = state.get("plan")
        test_plans = []
        
        # Generate tests for main files (skip test files themselves)
        for file in plan.files:
            if "test" in file.path.lower():
                continue
                
            logger.info(f"🧪 Generating tests for: {file.path}")
            
            try:
                code = read_file.run(file.path, project_name=project_name)
                if not code or "ERROR" in code:
                    continue
                
                ext = Path(file.path).suffix
                language_map = {
                    ".py": "python", ".js": "javascript", ".jsx": "javascript",
                    ".ts": "typescript", ".tsx": "typescript"
                }
                language = language_map.get(ext, "unknown")
                
                if language == "unknown":
                    continue
                
                tester_llm = get_tester_llm()
                test_plan = tester_llm.with_structured_output(TestPlan).invoke(
                    tester_prompt(file.path, code, language)
                )
                
                test_plans.append(test_plan)
                
                # Write test file
                test_filename = f"test_{Path(file.path).stem}{ext}"
                test_dir = "tests" if language == "python" else "__tests__"
                test_path = f"{test_dir}/{test_filename}"
                
                test_content = f"# Generated tests for {file.path}\n\n"
                for test_case in test_plan.test_cases:
                    test_content += f"# Test: {test_case.name}\n"
                    test_content += f"# {test_case.description}\n"
                    test_content += f"{test_case.code}\n\n"
                
                write_file.run(test_path, test_content, project_name=project_name)
                logger.success(f"✅ Generated {len(test_plan.test_cases)} tests for {file.path}")
                
            except Exception as e:
                logger.error(f"Error generating tests for {file.path}: {str(e)}")
        
        log_agent_complete("Tester", {"test_plans": len(test_plans)})
        
        # Update metadata
        metadata = state.get("metadata")
        if metadata:
            metadata.tests_generated = True
        
        return {
            **state,
            "status": "TEST_DONE",
            "test_plans": test_plans,
            "metadata": metadata
        }
    except Exception as e:
        log_agent_error("Tester", e)
        return {**state, "status": "TEST_DONE", "test_plans": []}


def finalization_agent(state: dict) -> dict:
    """Finalizes the project with git, docker, and other configurations."""
    log_agent_start("Finalization", state)
    
    try:
        project_name = state.get("project_name")
        plan: Plan = state.get("plan")
        metadata: ProjectMetadata = state.get("metadata")
        
        # Initialize git
        if app_config.enable_git:
            logger.info("🔧 Initializing Git repository...")
            git_init.run(project_name=project_name)
            git_commit.run("Initial commit: Project generated by Multi-Agent System", project_name=project_name)
            metadata.git_initialized = True
        
        # Generate requirements/package files
        if plan.required_packages:
            logger.info(f"📦 Generating dependency files...")
            if "python" in plan.techstack.lower():
                generate_requirements_txt.run(plan.required_packages, project_name=project_name)
            elif any(x in plan.techstack.lower() for x in ["javascript", "node", "react", "vue"]):
                deps = {pkg: "latest" for pkg in plan.required_packages}
                generate_package_json.run(plan.name, deps, project_name=project_name)
            
            metadata.packages_installed = plan.required_packages
        
        # Generate Docker configuration
        if plan.enable_docker or app_config.enable_docker:
            logger.info("🐳 Generating Docker configuration...")
            language = "python" if "python" in plan.techstack.lower() else "node"
            generate_dockerfile.run(language, project_name=project_name)
            generate_docker_compose.run([], project_name=project_name)
            metadata.docker_enabled = True
        
        # Generate CI/CD configuration
        if plan.enable_ci_cd:
            logger.info("⚙️  Generating CI/CD configuration...")
            generate_github_actions_workflow.run(project_name=project_name)
        
        # Count files and lines
        files_list = list_files.run(".", project_name=project_name)
        metadata.files_created = files_list.split("\n") if files_list else []
        
        log_agent_complete("Finalization", metadata)
        log_project_summary(project_name, len(metadata.files_created), metadata.total_lines)
        
        return {
            **state,
            "status": "DONE",
            "metadata": metadata
        }
    except Exception as e:
        log_agent_error("Finalization", e)
        return {**state, "status": "DONE"}


# Build the graph
graph = StateGraph(dict)

# Add nodes
graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)
graph.add_node("reviewer", reviewer_agent)
graph.add_node("tester", tester_agent)
graph.add_node("finalization", finalization_agent)

# Add edges
graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")

# Conditional edge for coder - loop until done
graph.add_conditional_edges(
    "coder",
    lambda s: s.get("status", "CONTINUE"),
    {
        "CODING_DONE": "reviewer",
        "CONTINUE": "coder"
    }
)

graph.add_edge("reviewer", "tester")
graph.add_edge("tester", "finalization")
graph.add_edge("finalization", END)

# Set entry point
graph.set_entry_point("planner")

# Compile with checkpointing (if available)
try:
    checkpoint_dir = Path(app_config.checkpoint_dir)
    checkpoint_dir.mkdir(exist_ok=True)
    from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
    import asyncio
    
    # Try to create checkpointer
    try:
        checkpointer = AsyncSqliteSaver.from_conn_string(str(checkpoint_dir / "checkpoints.db"))
        agent = graph.compile(checkpointer=checkpointer)
    except:
        # Fall back to no checkpointing
        logger.warning("Checkpointing unavailable, compiling without state persistence")
        agent = graph.compile()
except ImportError:
    logger.warning("Checkpointing unavailable, compiling without state persistence")
    agent = graph.compile()


if __name__ == "__main__":
    import sys
    project_name = sys.argv[1] if len(sys.argv) > 1 else "test_project"
    
    from agent.tools_enhanced import set_project_root
    set_project_root(project_name)
    
    result = agent.invoke(
        {
            "user_prompt": "Build a modern todo app with FastAPI backend and React frontend",
            "project_name": project_name
        },
        {"recursion_limit": app_config.max_recursion_limit}
    )
    print("\n🎉 Project Generation Complete!")
    print(f"Final State: {result.get('status')}")
