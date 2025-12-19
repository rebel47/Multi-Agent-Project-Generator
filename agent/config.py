"""
Configuration management for multi-model support and application settings.
"""
import os
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class ModelProvider(str, Enum):
    """Supported LLM providers"""
    GEMINI = "gemini"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"


class ModelConfig(BaseModel):
    """Configuration for LLM models"""
    provider: ModelProvider = Field(default=ModelProvider.GEMINI)
    model_name: str = Field(default="gemini-2.0-flash-exp")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None)
    streaming: bool = Field(default=True)
    
    # API Keys
    gemini_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY"))
    openai_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    anthropic_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"))
    groq_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("GROQ_API_KEY"))


class AgentConfig(BaseModel):
    """Configuration for different agents"""
    planner_model: ModelConfig = Field(default_factory=lambda: ModelConfig(
        provider=ModelProvider.GEMINI,
        model_name="gemini-2.0-flash-exp",
        temperature=0.7
    ))
    architect_model: ModelConfig = Field(default_factory=lambda: ModelConfig(
        provider=ModelProvider.GEMINI,
        model_name="gemini-2.0-flash-exp",
        temperature=0.5
    ))
    coder_model: ModelConfig = Field(default_factory=lambda: ModelConfig(
        provider=ModelProvider.GEMINI,
        model_name="gemini-2.0-flash-exp",
        temperature=0.3
    ))
    reviewer_model: ModelConfig = Field(default_factory=lambda: ModelConfig(
        provider=ModelProvider.GEMINI,
        model_name="gemini-2.0-flash-exp",
        temperature=0.2
    ))
    tester_model: ModelConfig = Field(default_factory=lambda: ModelConfig(
        provider=ModelProvider.GEMINI,
        model_name="gemini-2.0-flash-exp",
        temperature=0.4
    ))


class ApplicationConfig(BaseModel):
    """Main application configuration"""
    agent_config: AgentConfig = Field(default_factory=AgentConfig)
    
    # Feature flags
    enable_code_review: bool = Field(default=True)
    enable_testing: bool = Field(default=True)
    enable_git: bool = Field(default=True)
    enable_web_search: bool = Field(default=False)
    enable_docker: bool = Field(default=False)
    
    # Paths
    generated_projects_dir: str = Field(default="generated_project")
    templates_dir: str = Field(default="templates")
    checkpoint_dir: str = Field(default="checkpoints")
    
    # Limits
    max_recursion_limit: int = Field(default=100)
    max_file_size: int = Field(default=1024 * 1024)  # 1MB
    
    # Logging
    log_level: str = Field(default="INFO")
    enable_debug: bool = Field(default=False)
    enable_verbose: bool = Field(default=False)


def get_llm_from_config(config: ModelConfig):
    """Factory function to create LLM instance from config"""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
    except ImportError:
        ChatGoogleGenerativeAI = None
    try:
        from langchain_openai import ChatOpenAI
    except ImportError:
        ChatOpenAI = None
    try:
        from langchain_anthropic import ChatAnthropic
    except ImportError:
        ChatAnthropic = None
    try:
        from langchain_groq import ChatGroq
    except ImportError:
        ChatGroq = None
    
    common_params = {
        "temperature": config.temperature,
        "streaming": config.streaming,
    }
    
    if config.max_tokens:
        common_params["max_tokens"] = config.max_tokens
    
    if config.provider == ModelProvider.GEMINI:
        if not ChatGoogleGenerativeAI:
            raise ImportError("langchain-google-genai not installed. Run: pip install langchain-google-genai")
        if not config.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        return ChatGoogleGenerativeAI(
            model=config.model_name,
            google_api_key=config.gemini_api_key,
            **common_params
        )
    
    elif config.provider == ModelProvider.OPENAI:
        if not ChatOpenAI:
            raise ImportError("langchain-openai not installed. Run: pip install langchain-openai")
        if not config.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        return ChatOpenAI(
            model=config.model_name,
            api_key=config.openai_api_key,
            **common_params
        )
    
    elif config.provider == ModelProvider.ANTHROPIC:
        if not ChatAnthropic:
            raise ImportError("langchain-anthropic not installed. Run: pip install langchain-anthropic")
        if not config.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        return ChatAnthropic(
            model=config.model_name,
            api_key=config.anthropic_api_key,
            **common_params
        )
    
    elif config.provider == ModelProvider.GROQ:
        if not ChatGroq:
            raise ImportError("langchain-groq not installed. Run: pip install langchain-groq")
        if not config.groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        return ChatGroq(
            model=config.model_name,
            api_key=config.groq_api_key,
            **common_params
        )
    
    else:
        raise ValueError(f"Unsupported provider: {config.provider}")


# Global application config instance
app_config = ApplicationConfig()


def load_config_from_file(config_path: str = "config.yaml") -> ApplicationConfig:
    """Load configuration from YAML file"""
    import yaml
    from pathlib import Path
    
    config_file = Path(config_path)
    if config_file.exists():
        with open(config_file, 'r') as f:
            config_data = yaml.safe_load(f)
            return ApplicationConfig(**config_data)
    return ApplicationConfig()


def save_config_to_file(config: ApplicationConfig, config_path: str = "config.yaml"):
    """Save configuration to YAML file"""
    import yaml
    from pathlib import Path
    
    with open(config_path, 'w') as f:
        yaml.dump(config.model_dump(), f, default_flow_style=False)
