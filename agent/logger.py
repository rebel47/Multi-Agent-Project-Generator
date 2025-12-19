"""
Enhanced logging configuration with structured logging and progress tracking.
"""
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
from loguru import logger
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.table import Table

# Initialize rich console
console = Console()

# Configure loguru logger
logger.remove()  # Remove default handler

# Add custom handlers
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True
)

# Add file logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logger.add(
    log_dir / "agent_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="7 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    backtrace=True,
    diagnose=True
)


class AgentProgress:
    """Progress tracking for multi-agent system"""
    
    def __init__(self):
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        )
        self.current_task = None
        self.tasks = {}
    
    def __enter__(self):
        self.progress.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.progress.__exit__(exc_type, exc_val, exc_tb)
    
    def add_task(self, description: str, total: Optional[int] = None) -> int:
        """Add a new task to track"""
        task_id = self.progress.add_task(description, total=total)
        self.tasks[description] = task_id
        return task_id
    
    def update_task(self, task_id: int, advance: int = 1, description: Optional[str] = None):
        """Update task progress"""
        kwargs = {"advance": advance}
        if description:
            kwargs["description"] = description
        self.progress.update(task_id, **kwargs)
    
    def complete_task(self, task_id: int):
        """Mark task as complete"""
        self.progress.update(task_id, completed=True)


def log_agent_start(agent_name: str, state: dict):
    """Log when an agent starts execution"""
    logger.info(f"🤖 Starting {agent_name} agent")
    console.print(Panel(
        f"[bold cyan]{agent_name.upper()} AGENT[/bold cyan]",
        border_style="cyan"
    ))


def log_agent_complete(agent_name: str, result: dict):
    """Log when an agent completes execution"""
    logger.success(f"✅ {agent_name} agent completed")


def log_agent_error(agent_name: str, error: Exception):
    """Log when an agent encounters an error"""
    logger.error(f"❌ {agent_name} agent failed: {str(error)}")
    console.print(f"[bold red]Error in {agent_name}:[/bold red] {str(error)}")


def log_file_operation(operation: str, filepath: str, success: bool = True):
    """Log file operations"""
    emoji = "📝" if success else "❌"
    level = "info" if success else "error"
    getattr(logger, level)(f"{emoji} {operation}: {filepath}")


def log_model_call(model_name: str, tokens: Optional[int] = None):
    """Log LLM API calls"""
    msg = f"🤖 LLM Call: {model_name}"
    if tokens:
        msg += f" ({tokens} tokens)"
    logger.debug(msg)


def log_project_summary(project_name: str, files_created: int, total_lines: int):
    """Log final project summary"""
    table = Table(title=f"Project: {project_name}", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Files Created", str(files_created))
    table.add_row("Total Lines", str(total_lines))
    table.add_row("Status", "✅ Complete")
    
    console.print(table)


def log_cost_estimate(total_tokens: int, estimated_cost: float):
    """Log token usage and cost estimate"""
    logger.info(f"💰 Total tokens: {total_tokens:,} | Estimated cost: ${estimated_cost:.4f}")


class TokenTracker:
    """Track token usage across agents"""
    
    def __init__(self):
        self.total_tokens = 0
        self.agent_tokens = {}
    
    def add_tokens(self, agent_name: str, tokens: int):
        """Add tokens for an agent"""
        self.total_tokens += tokens
        self.agent_tokens[agent_name] = self.agent_tokens.get(agent_name, 0) + tokens
    
    def get_summary(self) -> dict:
        """Get token usage summary"""
        return {
            "total": self.total_tokens,
            "by_agent": self.agent_tokens,
            "estimated_cost": self.estimate_cost()
        }
    
    def estimate_cost(self, cost_per_1k_tokens: float = 0.0015) -> float:
        """Estimate cost based on token usage"""
        return (self.total_tokens / 1000) * cost_per_1k_tokens


# Global token tracker
token_tracker = TokenTracker()
