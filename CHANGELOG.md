# Changelog

All notable changes to the Multi-Agent Project Generator will be documented in this file.

## [2.0.0] - 2025-12-19

### 🎉 Major Release - Complete Rewrite

This is a major upgrade with 10+ new features and complete architecture overhaul.

### ✨ Added

#### Multi-Model Support
- Support for 4 LLM providers: Gemini, OpenAI, Anthropic, Groq
- Per-agent model configuration
- Automatic provider switching
- Cost tracking and estimation

#### New Agents
- **Code Reviewer Agent**: Automated code quality analysis
  - Quality scoring (0-100)
  - Security vulnerability detection
  - Best practices validation
  - Actionable improvement suggestions
  
- **Testing Agent**: Automatic test generation
  - Unit test creation for all code files
  - Multiple framework support (pytest, jest, etc.)
  - Edge case coverage
  - Test file organization

- **Finalization Agent**: Project finalization
  - Git repository initialization
  - Dependency file generation
  - Docker configuration
  - CI/CD setup

#### Advanced Tools
- Git integration (init, commit, status)
- Package management (pip, npm)
- Docker generation (Dockerfile, compose)
- CI/CD workflows (GitHub Actions)
- Web search capability (DuckDuckGo)
- Documentation fetching

#### User Interface
- **Gradio Web UI**: Beautiful web interface
  - Visual project configuration
  - Template browser with previews
  - Real-time progress tracking
  - Project file browser
  - Code viewer
  
#### Project Templates
- 7 production-ready templates:
  - FastAPI REST API
  - React SPA
  - Django Web App
  - Flask Microservice
  - Next.js Full-Stack
  - Python CLI Tool
  - Data Pipeline

#### Enhanced CLI
- Template support (`--template`)
- Feature flags (`--review`, `--test`, `--git`, `--docker`)
- Model selection (`--provider`, `--model`)
- List templates (`--list-templates`)
- Launch UI (`--ui`)
- 20+ command-line options

#### State Management
- LangGraph checkpointing with SQLite
- Resume interrupted workflows
- State persistence across sessions

#### Logging & Observability
- Structured logging with Loguru
- Rich terminal output with progress bars
- Token usage tracking
- Cost estimation
- Detailed log files
- Real-time status updates

#### Configuration
- YAML configuration file support
- Per-agent model settings
- Feature flag management
- Environment-based config

### 🔧 Improved

- **Prompts**: Enhanced prompts for all agents with better instructions
- **State Models**: Extended with review/test support
- **Error Handling**: Comprehensive error handling and recovery
- **Documentation**: Complete README rewrite with examples
- **Security**: Enhanced sandboxing and validation
- **Performance**: Optimized agent workflows

### 📚 Documentation

- Comprehensive README with 20+ sections
- CLI usage examples
- Template documentation
- Troubleshooting guide
- Performance metrics
- Cost analysis
- Best practices guide

### 🔄 Changed

- Upgraded to new LangGraph patterns
- Migrated from single to multi-model support
- Enhanced agent communication with richer state
- Improved file structure with separation of concerns

### 🐛 Fixed

- Path resolution issues
- Error propagation in agent chain
- Token tracking accuracy
- File permission handling

---

## [1.0.0] - 2024-11-15

### Initial Release

#### Features
- 3-agent system (Planner, Architect, Coder)
- Google Gemini integration
- Basic file operations
- Project generation from prompts
- CLI interface
- Project sandboxing

---

## Version History

- **v2.0.0** (2025-12-19): Complete rewrite with 6 agents, multi-model, UI, templates
- **v1.0.0** (2024-11-15): Initial release with basic 3-agent system

## Upgrade Guide

### From v1.0.0 to v2.0.0

**Breaking Changes:**
- `agent/graph.py` replaced with `agent/graph_enhanced.py`
- `agent/tools.py` replaced with `agent/tools_enhanced.py`
- New dependencies required (see requirements.txt)
- Environment variables now support multiple providers

**Migration Steps:**

1. Update dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Update `.env` file with new format:
   ```env
   GEMINI_API_KEY=your_key
   # Optional: Add other providers
   OPENAI_API_KEY=your_key
   ```

3. Update imports in custom code:
   ```python
   # Old
   from agent.graph import agent
   
   # New
   from agent.graph_enhanced import agent
   ```

4. Use new CLI options:
   ```bash
   # Old
   python main.py -r 100
   
   # New (backward compatible)
   python main.py --recursion-limit 100
   
   # Or use new features
   python main.py --template fastapi-rest-api --name my-api
   ```

**New Features Available:**
- Use `--ui` to launch web interface
- Use `--template` to start from templates
- Use `--provider` to switch LLM providers
- Enable/disable features with flags

**Legacy Support:**
- Original `graph.py` still available for compatibility
- Old CLI commands still work
- Gradual migration recommended
