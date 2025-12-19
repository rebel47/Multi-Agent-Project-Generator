"""
Advanced tools for code generation, git integration, package management, and web search.
"""
import pathlib
import subprocess
import json
import requests
from typing import Tuple, Optional, List, Dict
from langchain_core.tools import tool

# Dynamic project root, set per project
PROJECT_ROOT = None

def set_project_root(project_name: str):
    global PROJECT_ROOT
    PROJECT_ROOT = pathlib.Path.cwd() / "generated_project" / project_name
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    return str(PROJECT_ROOT)


def safe_path_for_project(path: str, project_name: str = None) -> pathlib.Path:
    global PROJECT_ROOT
    if PROJECT_ROOT is None:
        if not project_name:
            raise ValueError("PROJECT_ROOT not set and no project_name provided.")
        set_project_root(project_name)
    p = (PROJECT_ROOT / path).resolve()
    if PROJECT_ROOT.resolve() not in p.parents and PROJECT_ROOT.resolve() != p.parent and PROJECT_ROOT.resolve() != p:
        raise ValueError("Attempt to write outside project root")
    return p


@tool
def write_file(path: str, content: str, project_name: str = None) -> str:
    """Writes content to a file at the specified path within the project root."""
    from agent.logger import log_file_operation
    try:
        p = safe_path_for_project(path, project_name)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        log_file_operation("WRITE", str(p), success=True)
        return f"✅ WROTE: {p}"
    except Exception as e:
        log_file_operation("WRITE", path, success=False)
        return f"❌ ERROR writing {path}: {str(e)}"


@tool
def read_file(path: str, project_name: str = None) -> str:
    """Reads content from a file at the specified path within the project root."""
    from agent.logger import log_file_operation
    try:
        p = safe_path_for_project(path, project_name)
        if not p.exists():
            return ""
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
        log_file_operation("READ", str(p), success=True)
        return content
    except Exception as e:
        log_file_operation("READ", path, success=False)
        return f"❌ ERROR reading {path}: {str(e)}"


@tool
def get_current_directory(project_name: str = None) -> str:
    """Returns the current working directory."""
    global PROJECT_ROOT
    if PROJECT_ROOT is None:
        if not project_name:
            raise ValueError("PROJECT_ROOT not set and no project_name provided.")
        set_project_root(project_name)
    return str(PROJECT_ROOT)


@tool
def list_files(directory: str = ".", project_name: str = None) -> str:
    """Lists all files in the specified directory within the project root."""
    try:
        p = safe_path_for_project(directory, project_name)
        if not p.is_dir():
            return f"ERROR: {p} is not a directory"
        files = [str(f.relative_to(PROJECT_ROOT)) for f in p.glob("**/*") if f.is_file()]
        return "\n".join(files) if files else "No files found."
    except Exception as e:
        return f"❌ ERROR listing files: {str(e)}"


@tool
def run_cmd(cmd: str, cwd: str = None, timeout: int = 30) -> str:
    """Runs a shell command in the specified directory and returns the result."""
    try:
        cwd_dir = safe_path_for_project(cwd) if cwd else PROJECT_ROOT
        res = subprocess.run(cmd, shell=True, cwd=str(cwd_dir), capture_output=True, text=True, timeout=timeout)
        output = f"Return code: {res.returncode}\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"
        return output
    except subprocess.TimeoutExpired:
        return f"❌ Command timed out after {timeout} seconds"
    except Exception as e:
        return f"❌ ERROR running command: {str(e)}"


# === GIT INTEGRATION TOOLS ===

@tool
def git_init(project_name: str = None) -> str:
    """Initialize a git repository in the project directory."""
    try:
        project_dir = safe_path_for_project(".", project_name)
        result = subprocess.run(
            ["git", "init"],
            cwd=str(project_dir),
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            # Create .gitignore
            gitignore_content = """__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
*.so
*.egg
*.egg-info/
dist/
build/
.env
.venv
node_modules/
.DS_Store
*.log
"""
            gitignore_path = project_dir / ".gitignore"
            with open(gitignore_path, "w") as f:
                f.write(gitignore_content)
            
            return f"✅ Git repository initialized at {project_dir}"
        return f"❌ Git init failed: {result.stderr}"
    except Exception as e:
        return f"❌ ERROR initializing git: {str(e)}"


@tool
def git_commit(message: str, project_name: str = None) -> str:
    """Stage all changes and commit with the given message."""
    try:
        project_dir = safe_path_for_project(".", project_name)
        
        # Add all files
        subprocess.run(["git", "add", "."], cwd=str(project_dir), check=True)
        
        # Commit
        result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=str(project_dir),
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return f"✅ Committed: {message}"
        return f"❌ Commit failed: {result.stderr}"
    except Exception as e:
        return f"❌ ERROR committing: {str(e)}"


@tool
def git_status(project_name: str = None) -> str:
    """Get the git status of the project."""
    try:
        project_dir = safe_path_for_project(".", project_name)
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=str(project_dir),
            capture_output=True,
            text=True
        )
        return result.stdout if result.stdout else "Working tree clean"
    except Exception as e:
        return f"❌ ERROR getting git status: {str(e)}"


# === PACKAGE MANAGEMENT TOOLS ===

@tool
def install_python_package(package_name: str, project_name: str = None) -> str:
    """Install a Python package using pip."""
    try:
        result = subprocess.run(
            ["pip", "install", package_name],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return f"✅ Installed {package_name}"
        return f"❌ Failed to install {package_name}: {result.stderr}"
    except Exception as e:
        return f"❌ ERROR installing package: {str(e)}"


@tool
def generate_requirements_txt(packages: List[str], project_name: str = None) -> str:
    """Generate a requirements.txt file with the specified packages."""
    try:
        requirements_path = safe_path_for_project("requirements.txt", project_name)
        with open(requirements_path, "w") as f:
            for package in packages:
                f.write(f"{package}\n")
        return f"✅ Generated requirements.txt with {len(packages)} packages"
    except Exception as e:
        return f"❌ ERROR generating requirements.txt: {str(e)}"


@tool
def install_npm_package(package_name: str, project_name: str = None, dev: bool = False) -> str:
    """Install an npm package."""
    try:
        project_dir = safe_path_for_project(".", project_name)
        cmd = ["npm", "install"]
        if dev:
            cmd.append("--save-dev")
        cmd.append(package_name)
        
        result = subprocess.run(
            cmd,
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            return f"✅ Installed npm package: {package_name}"
        return f"❌ Failed to install {package_name}: {result.stderr}"
    except Exception as e:
        return f"❌ ERROR installing npm package: {str(e)}"


@tool
def generate_package_json(name: str, dependencies: Dict[str, str], project_name: str = None) -> str:
    """Generate a package.json file for Node.js projects."""
    try:
        package_json_path = safe_path_for_project("package.json", project_name)
        package_data = {
            "name": name,
            "version": "1.0.0",
            "description": f"Generated project: {name}",
            "main": "index.js",
            "scripts": {
                "start": "node index.js",
                "dev": "nodemon index.js"
            },
            "dependencies": dependencies,
            "devDependencies": {}
        }
        
        with open(package_json_path, "w") as f:
            json.dump(package_data, f, indent=2)
        
        return f"✅ Generated package.json"
    except Exception as e:
        return f"❌ ERROR generating package.json: {str(e)}"


# === WEB SEARCH TOOL ===

@tool
def web_search(query: str, num_results: int = 3) -> str:
    """Search the web for information using DuckDuckGo."""
    try:
        from duckduckgo_search import DDGS
        
        ddgs = DDGS()
        results = list(ddgs.text(query, max_results=num_results))
        
        if not results:
            return "No results found"
        
        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"{i}. {result['title']}\n"
                f"   URL: {result['href']}\n"
                f"   {result['body']}\n"
            )
        
        return "\n".join(formatted_results)
    except Exception as e:
        return f"❌ ERROR searching web: {str(e)}"


@tool
def fetch_documentation(url: str) -> str:
    """Fetch documentation from a URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Simple text extraction (could be enhanced with BeautifulSoup)
        content = response.text[:5000]  # Limit to first 5000 chars
        return f"Documentation from {url}:\n\n{content}"
    except Exception as e:
        return f"❌ ERROR fetching documentation: {str(e)}"


# === DOCKER GENERATION TOOLS ===

@tool
def generate_dockerfile(language: str, project_name: str = None) -> str:
    """Generate a Dockerfile based on the project language."""
    try:
        dockerfiles = {
            "python": """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
""",
            "node": """FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000
CMD ["node", "index.js"]
""",
            "react": """FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""
        }
        
        dockerfile_content = dockerfiles.get(language.lower(), dockerfiles["python"])
        dockerfile_path = safe_path_for_project("Dockerfile", project_name)
        
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_content)
        
        return f"✅ Generated Dockerfile for {language}"
    except Exception as e:
        return f"❌ ERROR generating Dockerfile: {str(e)}"


@tool
def generate_docker_compose(services: List[str], project_name: str = None) -> str:
    """Generate a docker-compose.yml file."""
    try:
        compose_content = """version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - ENV=development
"""
        
        compose_path = safe_path_for_project("docker-compose.yml", project_name)
        with open(compose_path, "w") as f:
            f.write(compose_content)
        
        return f"✅ Generated docker-compose.yml"
    except Exception as e:
        return f"❌ ERROR generating docker-compose.yml: {str(e)}"


@tool
def generate_github_actions_workflow(project_name: str = None) -> str:
    """Generate a GitHub Actions CI/CD workflow."""
    try:
        workflow_content = """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest tests/ -v
    
    - name: Lint code
      run: |
        pip install flake8
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
"""
        
        workflows_dir = safe_path_for_project(".github/workflows", project_name)
        workflows_dir.mkdir(parents=True, exist_ok=True)
        
        workflow_path = workflows_dir / "ci.yml"
        with open(workflow_path, "w") as f:
            f.write(workflow_content)
        
        return f"✅ Generated GitHub Actions workflow"
    except Exception as e:
        return f"❌ ERROR generating GitHub Actions workflow: {str(e)}"


def init_project_root(project_name: str):
    return set_project_root(project_name)
