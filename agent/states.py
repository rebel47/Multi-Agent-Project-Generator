from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class File(BaseModel):
    path: str = Field(description="The path to the file to be created or modified")
    purpose: str = Field(description="The purpose of the file, e.g. 'main application logic', 'data processing module', etc.")
    dependencies: Optional[List[str]] = Field(default=[], description="List of other files this file depends on")
    

class Plan(BaseModel):
    name: str = Field(description="The name of app to be built")
    description: str = Field(description="A oneline description of the app to be built, e.g. 'A web application for managing personal finances'")
    techstack: str = Field(description="The tech stack to be used for the app, e.g. 'python', 'javascript', 'react', 'flask', etc.")
    features: list[str] = Field(description="A list of features that the app should have, e.g. 'user authentication', 'data visualization', etc.")
    files: list[File] = Field(description="A list of files to be created, each with a 'path' and 'purpose'")
    required_packages: Optional[List[str]] = Field(default=[], description="List of required packages/dependencies")
    enable_docker: Optional[bool] = Field(default=False, description="Whether to generate Docker configuration")
    enable_ci_cd: Optional[bool] = Field(default=False, description="Whether to generate CI/CD configuration")


class ImplementationTask(BaseModel):
    filepath: str = Field(description="The path to the file to be modified")
    task_description: str = Field(description="A detailed description of the task to be performed on the file, e.g. 'add user authentication', 'implement data processing logic', etc.")
    priority: Optional[int] = Field(default=0, description="Priority of the task (higher = more important)")
    estimated_complexity: Optional[str] = Field(default="medium", description="Estimated complexity: low, medium, high")


class TaskPlan(BaseModel):
    implementation_steps: list[ImplementationTask] = Field(description="A list of steps to be taken to implement the task")
    model_config = ConfigDict(extra="allow")
    

class CoderState(BaseModel):
    task_plan: TaskPlan = Field(description="The plan for the task to be implemented")
    current_step_idx: int = Field(0, description="The index of the current step in the implementation steps")
    current_file_content: Optional[str] = Field(None, description="The content of the file currently being edited or created")


class CodeReviewResult(BaseModel):
    filepath: str = Field(description="The path to the file being reviewed")
    issues: List[str] = Field(default=[], description="List of issues found in the code")
    suggestions: List[str] = Field(default=[], description="List of improvement suggestions")
    quality_score: int = Field(description="Quality score from 0-100")
    approved: bool = Field(description="Whether the code is approved")
    

class TestCase(BaseModel):
    name: str = Field(description="Name of the test case")
    description: str = Field(description="Description of what the test validates")
    code: str = Field(description="Test code")
    

class TestPlan(BaseModel):
    filepath: str = Field(description="The file being tested")
    test_framework: str = Field(description="Testing framework to use (e.g., pytest, unittest, jest)")
    test_cases: List[TestCase] = Field(description="List of test cases")
    

class ProjectMetadata(BaseModel):
    """Metadata about the generated project"""
    project_name: str
    created_at: str
    files_created: List[str] = Field(default=[])
    total_lines: int = Field(default=0)
    packages_installed: List[str] = Field(default=[])
    git_initialized: bool = Field(default=False)
    docker_enabled: bool = Field(default=False)
    tests_generated: bool = Field(default=False)