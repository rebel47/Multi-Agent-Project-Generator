# 🤖 Multi-Agent Project Generator

An intelligent multi-agent system powered by **Multiple LLM Providers** and **LangGraph** that automatically generates complete, production-ready engineering projects from natural language descriptions. This system orchestrates multiple specialized AI agents to plan, architect, implement, review, and test full software projects with proper file structures and working code.

## ✨ What's New in v2.0

- 🎯 **Multi-Model Support**: Use OpenAI, Anthropic Claude, Google Gemini, or Groq
- 🔍 **Code Review Agent**: Automated code quality analysis and suggestions
- 🧪 **Testing Agent**: Automatic unit test generation
- 🌐 **Web UI**: Beautiful Gradio interface for easy project generation
- 📋 **Project Templates**: 7+ pre-built templates for common project types
- 🔧 **Git Integration**: Automatic repository initialization and commits
- 🐳 **Docker Support**: Auto-generate Dockerfiles and docker-compose
- ⚙️ **CI/CD Generation**: GitHub Actions workflows
- 📦 **Package Management**: Smart dependency detection and management
- 🔎 **Web Search**: Research capabilities for best practices
- 💾 **State Persistence**: Resume interrupted workflows with checkpointing
- 📊 **Rich Logging**: Beautiful terminal output with progress tracking
- 🎨 **Enhanced CLI**: Powerful command-line interface with many options

## 🌟 Features

### Core Features
- **Natural Language to Code**: Transform simple text descriptions into complete, working projects
- **Multi-Agent Architecture**: Specialized agents for planning, architecture, coding, review, and testing
- **Intelligent Planning**: Automatically determines optimal tech stacks and project structures
- **Task Decomposition**: Breaks down complex projects into manageable implementation tasks
- **File System Integration**: Creates proper directory structures and manages file operations
- **Structured Output**: Uses Pydantic models for reliable, type-safe agent communication

### Advanced Features
- **Multiple LLM Providers**: Choose from Gemini, OpenAI GPT-4, Claude, or Groq
- **Code Quality Assurance**: Automated review with quality scoring and suggestions
- **Automated Testing**: Generate comprehensive unit tests for all code
- **Version Control**: Automatic git initialization with meaningful commits
- **Containerization**: Docker and docker-compose generation
- **CI/CD Pipelines**: GitHub Actions workflow generation
- **Web Search Integration**: Research APIs and best practices during generation
- **Project Templates**: Quick start with 7+ production-ready templates
- **Web Interface**: User-friendly Gradio UI for non-technical users
- **Progress Tracking**: Real-time feedback with rich terminal output
- **State Checkpointing**: Resume projects after interruptions
- **Token Tracking**: Monitor API usage and cost estimation

## 🏗️ System Architecture

The system uses a **LangGraph state machine** with six specialized agents working in sequence:

### 1. **Planner Agent** 🎯
- **Role**: Converts user prompts into structured project plans
- **Input**: Natural language project description
- **Output**: Complete project specification with tech stack, features, and file structure
- **Model**: Configurable (Gemini/GPT-4/Claude)

### 2. **Architect Agent** 🏛️
- **Role**: Creates detailed implementation roadmap
- **Input**: Project plan from Planner
- **Output**: Ordered task list with dependencies and implementation details
- **Features**: Dependency resolution, priority assignment, complexity estimation

### 3. **Coder Agent** 💻
- **Role**: Implements code using ReAct pattern with tools
- **Tools**: File I/O, git, package management, web search
- **Output**: Complete, working codebase
- **Features**: Context-aware coding, best practices, error handling

### 4. **Reviewer Agent** 🔍
- **Role**: Validates code quality and identifies issues
- **Analysis**: Quality, security, performance, best practices
- **Output**: Quality score, issues list, improvement suggestions
- **Features**: Language-specific conventions, security scanning

### 5. **Tester Agent** 🧪
- **Role**: Generates comprehensive unit tests
- **Coverage**: Happy paths, edge cases, error handling
- **Output**: Complete test files with multiple test cases
- **Frameworks**: pytest, unittest, jest, mocha

### 6. **Finalization Agent** 🎁
- **Role**: Adds git, Docker, CI/CD, and dependencies
- **Actions**: Git init/commit, generate configs, package files
- **Output**: Production-ready project with all configurations

### Agent Communication Flow

```
User Input → Planner → Plan Object
                ↓
           Architect → TaskPlan Object
                ↓
             Coder → Complete Code
                ↓
           Reviewer → Quality Analysis
                ↓
            Tester → Test Suite
                ↓
        Finalization → Production-Ready Project
```

## 📋 Prerequisites

- **Python 3.9+** (Python 3.11+ recommended)
- **At least one LLM API Key**:
  - **Google Gemini** (get from [Google AI Studio](https://makersuite.google.com/app/apikey)) - **FREE**
  - **OpenAI** (get from [OpenAI Platform](https://platform.openai.com/api-keys))
  - **Anthropic Claude** (get from [Anthropic Console](https://console.anthropic.com/))
  - **Groq** (get from [Groq Console](https://console.groq.com/))
- **Internet Connection** (for API calls and web search)
- **Git** (optional, for version control features)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rebel47/Multi-Agent-Project-Generator.git
   cd Multi-Agent-Project-Generator
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   # Required: At least one API key
   GEMINI_API_KEY=your_gemini_api_key_here
   
   # Optional: Other providers
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

## 💻 Usage

### 🌐 Web UI (Recommended for Beginners)

Launch the beautiful Gradio web interface:

```bash
python main.py --ui
```

Then open your browser to `http://localhost:7860`

**Web UI Features:**
- Visual project configuration
- Template browser with previews
- Real-time generation progress
- Project file browser
- Code preview
- Easy settings management

**To share publicly:**
```bash
python main.py --ui --share
```

### 🖥️ Command Line Interface

#### **Basic Usage**

```bash
# Interactive mode
python main.py

# Direct prompt
python main.py --prompt "Create a REST API with FastAPI" --name my-api

# Use a template
python main.py --template fastapi-rest-api --name my-project
```

#### **Advanced Usage**

```bash
# Full-featured generation with all options
python main.py \
  --prompt "Build a todo app with authentication" \
  --name todo-app \
  --review \
  --test \
  --git \
  --docker \
  --provider openai \
  --model gpt-4 \
  --recursion-limit 150

# Use template with custom additions
python main.py \
  --template react-spa \
  --prompt "Add dark mode and user profiles" \
  --name my-react-app \
  --review \
  --test

# List all available templates
python main.py --list-templates

# Disable features
python main.py \
  --prompt "Simple calculator" \
  --name calc \
  --no-review \
  --no-test \
  --no-git
```

### 📋 CLI Options Reference

```
Project Specification:
  --prompt, -p TEXT        Project description
  --name, -n TEXT          Project name
  --template, -t NAME      Use a project template
  --list-templates, -l     List available templates

Features (enabled by default):
  --review                 Enable code review
  --no-review              Disable code review
  --test                   Generate unit tests
  --no-test                Skip test generation
  --git                    Initialize git repository
  --no-git                 Skip git initialization
  --docker                 Generate Docker configuration
  --web-search             Enable web search capability

Model Configuration:
  --provider TEXT          LLM provider (gemini/openai/anthropic/groq)
  --model TEXT             Model name (e.g., gpt-4, claude-3-opus)
  --recursion-limit, -r N  Max iterations (default: 100)

Web UI:
  --ui                     Launch web interface
  --port N                 Web UI port (default: 7860)
  --share                  Create public share link
```

### 📚 Available Templates

| Template | Description | Tech Stack |
|----------|-------------|------------|
| `fastapi-rest-api` | Modern REST API | Python, FastAPI, SQLAlchemy |
| `react-spa` | Single-page app | React, TypeScript, Material-UI |
| `django-webapp` | Full web application | Python, Django, PostgreSQL |
| `flask-microservice` | Lightweight service | Python, Flask, Redis |
| `nextjs-fullstack` | Full-stack app | Next.js, TypeScript, Prisma |
| `python-cli-tool` | Command-line tool | Python, Click, Rich |
| `data-pipeline` | ETL pipeline | Python, Airflow, Pandas |

**View template details:**
```bash
python main.py --list-templates
```

### 🎯 Usage Examples

**1. Quick Start with Template**
```bash
python main.py --template fastapi-rest-api --name my-api
```

**2. Custom Project with All Features**
```bash
python main.py \
  --prompt "E-commerce API with product catalog and orders" \
  --name ecommerce-api \
  --review \
  --test \
  --git \
  --docker \
  --provider openai \
  --model gpt-4
```

**3. Simple Project, No Extras**
```bash
python main.py \
  --prompt "Command line calculator" \
  --name calculator \
  --no-review \
  --no-test \
  --no-git
```

**4. Template + Custom Requirements**
```bash
python main.py \
  --template react-spa \
  --prompt "Add authentication, dark mode, and real-time updates" \
  --name my-app
```

**5. Using Different LLM Providers**

```bash
# With OpenAI GPT-4
python main.py --prompt "Blog platform" --name blog --provider openai --model gpt-4-turbo

# With Anthropic Claude
python main.py --prompt "Chat app" --name chat --provider anthropic --model claude-3-opus-20240229

# With Groq (fast and free)
python main.py --prompt "Todo app" --name todo --provider groq --model mixtral-8x7b-32768
```

## 📁 Project Structure

```
Multi-Agent-Project-Generator/
├── main.py                      # Enhanced CLI entry point
├── app.py                       # Gradio web UI
├── requirements.txt             # All dependencies
├── .env                         # API keys (create this)
├── README.md                    # This file
│
├── agent/                       # Agent implementation
│   ├── __init__.py
│   ├── graph.py                 # Original graph (legacy)
│   ├── graph_enhanced.py        # NEW: Enhanced multi-agent graph
│   ├── prompts.py               # Enhanced agent prompts
│   ├── states.py                # Enhanced state models
│   ├── tools.py                 # Original tools (legacy)
│   ├── tools_enhanced.py        # NEW: Advanced tools (git, docker, search)
│   ├── config.py                # NEW: Multi-model configuration
│   └── logger.py                # NEW: Rich logging and progress tracking
│
├── templates/                   # NEW: Project templates
│   └── __init__.py              # Template definitions
│
├── generated_project/           # Output directory
│   ├── project1/
│   ├── project2/
│   └── ...
│
├── checkpoints/                 # NEW: LangGraph state persistence
│   └── checkpoints.db
│
└── logs/                        # NEW: Application logs
    └── agent_2025-12-19.log
```

### Key Files Explained

**Core Files:**
- **`main.py`**: Enhanced CLI with templates, multi-model support, and all features
- **`app.py`**: Beautiful Gradio web interface for easy project generation
- **`requirements.txt`**: Complete dependency list including new packages

**Agent System:**
- **`agent/graph_enhanced.py`**: New graph with 6 agents (planner, architect, coder, reviewer, tester, finalizer)
- **`agent/config.py`**: Multi-model configuration supporting 4+ LLM providers
- **`agent/logger.py`**: Structured logging with Rich terminal output
- **`agent/tools_enhanced.py`**: 20+ tools including git, docker, package management, web search
- **`agent/prompts.py`**: Enhanced prompts for all agents
- **`agent/states.py`**: Extended state models with review/test support

**Templates:**
- **`templates/__init__.py`**: 7 production-ready project templates

**Generated:**
- **`generated_project/`**: All generated projects (git-ignored)
- **`checkpoints/`**: State persistence for resume capability
- **`logs/`**: Detailed application logs

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
# Required: At least one API key
GEMINI_API_KEY=your_key_here

# Optional: Additional providers
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
```

### Advanced Configuration

Create a `config.yaml` file for persistent settings:

```yaml
agent_config:
  planner_model:
    provider: "gemini"
    model_name: "gemini-2.0-flash-exp"
    temperature: 0.7
  
  coder_model:
    provider: "openai"
    model_name: "gpt-4"
    temperature: 0.3

enable_code_review: true
enable_testing: true
enable_git: true
enable_docker: false
enable_web_search: false

max_recursion_limit: 100
log_level: "INFO"
```

### Feature Flags

| Feature | Default | Description |
|---------|---------|-------------|
| `enable_code_review` | `true` | Run code quality analysis |
| `enable_testing` | `true` | Generate unit tests |
| `enable_git` | `true` | Initialize git repo |
| `enable_docker` | `false` | Generate Docker configs |
| `enable_web_search` | `false` | Enable web research |
| `enable_debug` | `false` | Detailed debug logs |

## 🛡️ Security Features

- **Sandboxed File Operations**: All operations restricted to `generated_project/<project_name>`
- **Path Validation**: Prevents directory traversal attacks
- **Safe Command Execution**: Timeout and error handling for shell commands
- **API Key Protection**: Keys stored in `.env` (never committed)
- **Code Security Scanning**: Reviewer agent checks for common vulnerabilities
- **Input Validation**: Pydantic models validate all agent inputs/outputs

## 🔍 How It Works

### Generation Process

1. **Input Processing** 📝
   - User provides prompt or selects template
   - Configuration validated
   - Project root created

2. **Planning Phase** 🎯
   - Planner agent analyzes requirements
   - Determines tech stack and architecture
   - Creates complete file structure
   - Lists required dependencies

3. **Architecture Phase** 🏛️
   - Architect breaks plan into tasks
   - Orders tasks by dependencies
   - Assigns priorities and complexity
   - Creates detailed implementation guide

4. **Implementation Phase** 💻
   - Coder agent works through tasks
   - Uses tools (file I/O, git, packages)
   - Writes complete, working code
   - Maintains consistency across files

5. **Review Phase** 🔍
   - Reviewer analyzes each file
   - Checks quality, security, performance
   - Generates quality scores
   - Provides improvement suggestions

6. **Testing Phase** 🧪
   - Tester generates unit tests
   - Covers happy paths and edge cases
   - Creates runnable test files
   - Chooses appropriate framework

7. **Finalization Phase** 🎁
   - Initialize git repository
   - Generate dependency files
   - Create Docker configs
   - Set up CI/CD workflows
   - Commit initial version

### Technology Stack

- **LangGraph**: Agent workflow orchestration
- **LangChain**: LLM abstraction and tool integration
- **Pydantic**: Data validation and structured outputs
- **Loguru**: Structured logging
- **Rich**: Beautiful terminal output
- **Gradio**: Web UI framework
- **SQLite**: State persistence
- **Multiple LLMs**: Gemini, GPT-4, Claude, Groq

## 🐛 Troubleshooting

### Common Issues

**1. API Key Errors**
```
Error: GEMINI_API_KEY not found
```
**Solution**: Create `.env` file with your API key(s)

**2. Import Errors**
```
ModuleNotFoundError: No module named 'langchain'
```
**Solution**: 
```bash
pip install -r requirements.txt
```

**3. Recursion Limit Exceeded**
```
RecursionError: maximum recursion depth exceeded
```
**Solution**: Increase limit:
```bash
python main.py --recursion-limit 200
```

**4. Empty Project Name**
```
Project name cannot be empty
```
**Solution**: Provide valid name:
```bash
python main.py --name my-project
```

**5. Model Not Found**
```
Error: Model 'xyz' not found
```
**Solution**: Check model name for your provider:
- Gemini: `gemini-2.0-flash-exp`, `gemini-pro`
- OpenAI: `gpt-4`, `gpt-3.5-turbo`
- Anthropic: `claude-3-opus-20240229`, `claude-3-sonnet-20240229`
- Groq: `mixtral-8x7b-32768`, `llama2-70b-4096`

**6. Web UI Won't Start**
```
Error: Port 7860 already in use
```
**Solution**: Use different port:
```bash
python main.py --ui --port 8080
```

**7. Checkpoint Database Locked**
```
Error: Database is locked
```
**Solution**: Delete checkpoints and restart:
```bash
rm -rf checkpoints/
```

### Getting Help

- **Check logs**: `logs/agent_<date>.log`
- **Enable debug**: `python main.py --debug`
- **GitHub Issues**: [Report a bug](https://github.com/rebel47/Multi-Agent-Project-Generator/issues)

## 📊 Performance & Costs

### Token Usage

Typical project generation (10 files):
- **Planner**: ~1,500 tokens
- **Architect**: ~2,000 tokens  
- **Coder**: ~20,000 tokens (2,000 per file)
- **Reviewer**: ~10,000 tokens (1,000 per file)
- **Tester**: ~15,000 tokens (1,500 per file)
- **Total**: ~48,500 tokens

### Cost Estimates (per project)

| Provider | Model | Cost per 1M tokens | Typical Project Cost |
|----------|-------|-------------------|---------------------|
| Gemini | 2.0 Flash | **FREE** | **$0.00** |
| Groq | Mixtral 8x7B | **FREE** | **$0.00** |
| OpenAI | GPT-4 Turbo | $10 | ~$0.50 |
| OpenAI | GPT-3.5 Turbo | $0.50 | ~$0.025 |
| Anthropic | Claude 3 Opus | $15 | ~$0.75 |
| Anthropic | Claude 3 Sonnet | $3 | ~$0.15 |

**💡 Pro Tip**: Use Gemini or Groq for free, unlimited generation!

### Generation Time

- **Simple project** (3-5 files): 1-2 minutes
- **Medium project** (10-15 files): 3-5 minutes  
- **Complex project** (20+ files): 5-10 minutes

Times vary based on:
- Model provider and speed
- Project complexity
- Enabled features (review, testing)
- Internet connection speed

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Areas for Contribution

1. **New Templates**: Add templates for more frameworks
2. **LLM Providers**: Integrate additional providers
3. **Tools**: Add new capabilities (database setup, deployment, etc.)
4. **Testing**: Improve test generation quality
5. **UI**: Enhance the web interface
6. **Documentation**: Improve guides and examples
7. **Bug Fixes**: Report and fix issues

### Development Setup

```bash
# Clone repo
git clone https://github.com/rebel47/Multi-Agent-Project-Generator.git
cd Multi-Agent-Project-Generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dev dependencies
pip install -r requirements.txt
pip install pytest black ruff mypy

# Run tests
pytest tests/

# Format code
black .
ruff check .
```

### Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Format code (`black .`)
6. Commit changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📝 License

This project is created for **educational and research purposes**. Feel free to use, modify, and distribute as needed.

MIT License - see LICENSE file for details.

## 🎯 Roadmap

### v2.1 (Q1 2026)
- [ ] Support for more programming languages (Go, Rust, Java)
- [ ] Database schema generation and migrations
- [ ] API documentation generation (OpenAPI/Swagger)
- [ ] Enhanced refactoring capabilities
- [ ] Project update/modification mode
- [ ] Multi-file code analysis

### v2.2 (Q2 2026)
- [ ] Cloud deployment integration (AWS, GCP, Azure)
- [ ] Kubernetes configuration generation
- [ ] Monitoring and observability setup
- [ ] Load testing generation
- [ ] Security scanning integration
- [ ] Performance profiling

### v3.0 (Future)
- [ ] Visual project builder (drag-and-drop)
- [ ] Real-time collaboration
- [ ] Project marketplace and sharing
- [ ] Custom agent creation
- [ ] Plugin system
- [ ] IDE extensions (VSCode, JetBrains)

## 🙏 Acknowledgments

- Built with [LangChain](https://www.langchain.com/) and [LangGraph](https://langchain-ai.github.io/langgraph/)
- Powered by multiple LLM providers:
  - [Google Gemini AI](https://deepmind.google/technologies/gemini/)
  - [OpenAI GPT-4](https://openai.com/)
  - [Anthropic Claude](https://www.anthropic.com/)
  - [Groq](https://groq.com/)
- UI built with [Gradio](https://gradio.app/)
- Logging with [Loguru](https://github.com/Delgan/loguru) and [Rich](https://rich.readthedocs.io/)
- Inspired by autonomous agent research and software engineering automation

## 💡 Tips & Best Practices

### For Best Results

1. **Be Specific**: Detailed prompts produce better results
   - ❌ "Build a website"
   - ✅ "Build a portfolio website with blog, projects section, and contact form using React and Tailwind"

2. **Use Templates**: Start with templates for common patterns
   - Faster generation
   - Production-ready structure
   - Best practices included

3. **Review Generated Code**: Always review before deploying
   - Check security implications
   - Verify business logic
   - Test thoroughly

4. **Iterate**: Use generated code as a starting point
   - Customize to your needs
   - Add specific features
   - Refine architecture

5. **Choose Right Model**:
   - **Gemini/Groq**: Free, fast, good for most projects
   - **GPT-4**: Best quality, complex projects
   - **Claude**: Great for large context, detailed analysis
   - **GPT-3.5**: Fast and cheap for simple projects

### Project Types That Work Well

✅ **Great for:**
- REST APIs and microservices
- CRUD applications
- CLI tools and scripts
- Data pipelines
- Static websites and SPAs
- Bot and automation scripts
- Utility libraries

⚠️ **May need refinement:**
- Complex business logic
- Real-time systems
- High-performance applications
- ML/AI models
- Custom protocols
- Legacy system integration

## 🌟 Showcase

### Example Generated Projects

**1. E-Commerce API**
```bash
python main.py --template fastapi-rest-api --name ecommerce-api
```
- 15 files generated
- Product catalog, orders, authentication
- PostgreSQL database
- API documentation included
- Ready to deploy

**2. React Dashboard**
```bash
python main.py --template react-spa --name admin-dashboard --docker
```
- Modern React with TypeScript
- Material-UI components
- Dark mode support
- Docker containerized
- CI/CD ready

**3. Data Pipeline**
```bash
python main.py --template data-pipeline --name etl-pipeline --test
```
- Airflow DAGs
- Data validation
- Error handling
- Unit tests included
- Production-ready

## 📚 Additional Resources

### Documentation
- [LangGraph Guide](https://langchain-ai.github.io/langgraph/)
- [LangChain Docs](https://python.langchain.com/)
- [Agent Design Patterns](https://langchain-ai.github.io/langgraph/concepts/)

### Tutorials
- [Building Multi-Agent Systems](https://blog.langchain.dev/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [LLM Application Patterns](https://martinfowler.com/articles/patterns-of-distributed-systems/)

### Community
- [GitHub Discussions](https://github.com/rebel47/Multi-Agent-Project-Generator/discussions)
- [Issue Tracker](https://github.com/rebel47/Multi-Agent-Project-Generator/issues)

## 📧 Contact & Support

- **GitHub**: [@rebel47](https://github.com/rebel47)
- **Issues**: [Report bugs](https://github.com/rebel47/Multi-Agent-Project-Generator/issues)
- **Discussions**: [Ask questions](https://github.com/rebel47/Multi-Agent-Project-Generator/discussions)

## ⭐ Show Your Support

If you find this project useful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs and issues
- 💡 Suggesting new features
- 🤝 Contributing code
- 📢 Sharing with others

---

**Made with ❤️ by rebel47**

*Generate better software, faster.*
