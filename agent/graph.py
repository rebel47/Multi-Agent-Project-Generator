from dotenv import load_dotenv

# Handle deprecated langchain.globals import
try:
    from langchain.globals import set_verbose, set_debug
except ImportError:
    def set_verbose(v): pass
    def set_debug(d): pass

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent

from agent.prompts import *
from agent.states import *
from agent.tools import write_file, read_file, get_current_directory, list_files

_ = load_dotenv()

set_debug(True)
set_verbose(True)

import os

# Lazy LLM initialization - will be created on first use
_llm = None

def get_llm():
    """Get or create LLM instance (lazy initialization)"""
    global _llm
    if _llm is not None:
        return _llm
    
    # Try OpenAI first
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            from langchain_openai import ChatOpenAI
            _llm = ChatOpenAI(model="gpt-4", api_key=openai_key)
            return _llm
        except Exception:
            pass
    
    # Fall back to Gemini
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        try:
            _llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=gemini_key)
            return _llm
        except Exception:
            pass
    
    raise ValueError("No LLM API key found. Set OPENAI_API_KEY or GEMINI_API_KEY in .env")


def planner_agent(state: dict) -> dict:
    """Converts user prompt into a structured Plan."""
    user_prompt = state["user_prompt"]
    llm = get_llm()
    resp = llm.with_structured_output(Plan).invoke(
        planner_prompt(user_prompt)
    )
    if resp is None:
        raise ValueError("Planner did not return a valid response.")
    return {"plan": resp, "project_name": state.get("project_name")}


def architect_agent(state: dict) -> dict:
    """Creates TaskPlan from Plan."""
    plan: Plan = state["plan"]
    llm = get_llm()
    resp = llm.with_structured_output(TaskPlan).invoke(
        architect_prompt(plan=plan.model_dump_json())
    )
    if resp is None:
        raise ValueError("Planner did not return a valid response.")

    resp.plan = plan
    print(resp.model_dump_json())
    return {"task_plan": resp, "project_name": state.get("project_name")}


def coder_agent(state: dict) -> dict:
    """LangGraph tool-using coder agent."""
    coder_state: CoderState = state.get("coder_state")
    if coder_state is None:
        coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)

    steps = coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        return {"coder_state": coder_state, "status": "DONE", "project_name": state.get("project_name")}

    current_task = steps[coder_state.current_step_idx]
    project_name = state.get("project_name")
    existing_content = read_file.run(current_task.filepath, project_name=project_name)

    system_prompt = coder_system_prompt()
    user_prompt = (
        f"Task: {current_task.task_description}\n"
        f"File: {current_task.filepath}\n"
        f"Existing content:\n{existing_content}\n"
        "Use write_file(path, content) to save your changes."
    )

    coder_tools = [read_file, write_file, list_files, get_current_directory]
    llm = get_llm()
    react_agent = create_react_agent(llm, coder_tools)

    react_agent.invoke({"messages": [{"role": "system", "content": system_prompt},
                                     {"role": "user", "content": user_prompt}]})

    coder_state.current_step_idx += 1
    return {"coder_state": coder_state, "project_name": project_name}


graph = StateGraph(dict)

graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)

graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")
graph.add_conditional_edges(
    "coder",
    lambda s: "END" if s.get("status") == "DONE" else "coder",
    {"END": END, "coder": "coder"}
)

graph.set_entry_point("planner")
agent = graph.compile()
if __name__ == "__main__":
    import sys
    project_name = sys.argv[1] if len(sys.argv) > 1 else "default_project"
    result = agent.invoke({"user_prompt": "Build a colourful modern todo app in html css and js", "project_name": project_name},
                          {"recursion_limit": 100})
    print("Final State:", result)
