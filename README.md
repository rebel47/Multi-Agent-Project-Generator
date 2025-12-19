# 🤖 Multi Agent Project Generator

An intelligent multi-agent system powered by **Google Gemini AI** and **LangGraph** that automatically generates complete, production-ready engineering projects from natural language descriptions. This system orchestrates multiple specialized AI agents to plan, architect, and implement full software projects with proper file structures and working code.

## 🌟 Features

- **Natural Language to Code**: Transform simple text descriptions into complete, working projects
- **Multi-Agent Architecture**: Specialized agents for planning, architecture, and coding
- **🎨 Web Interface**: Beautiful Streamlit UI for easy project generation and browsing
- **📂 Project Browser**: View, explore, and download generated projects with file previews
- **🔄 Real-time Progress**: Watch agents work in real-time during generation
- **Intelligent Planning**: Automatically determines optimal tech stacks and project structures
- **Task Decomposition**: Breaks down complex projects into manageable implementation tasks
- **File System Integration**: Creates proper directory structures and manages file operations
- **Structured Output**: Uses Pydantic models for reliable, type-safe agent communication
- **Multi-LLM Support**: Works with OpenAI GPT-4 and Google Gemini (with fallbacks)
- **Configurable Recursion**: Adjustable recursion limits for handling complex projects
- **Multiple Tech Stacks**: Supports Python, JavaScript, React, Flask, FastAPI, and more
- **Isolated Projects**: Each generated project is stored in its own directory

## 🏗️ System Architecture

The system uses a **LangGraph state machine** with three specialized agents working in sequence:

### 1. **Planner Agent**
- **Role**: Converts user prompts into structured project plans
- **Input**: Natural language project description
- **Output**: `Plan` object containing:
  - Project name and description
  - Recommended tech stack
  - Feature list
  - File structure with purposes
- **Model**: Uses structured output with Pydantic validation

### 2. **Architect Agent**
- **Role**: Creates detailed implementation roadmap
- **Input**: `Plan` from Planner Agent
- **Output**: `TaskPlan` with step-by-step implementation tasks
- **Features**: 
  - Breaks down high-level plan into actionable tasks
  - Determines file dependencies and implementation order
  - Specifies detailed task descriptions for each file

### 3. **Coder Agent**
- **Role**: Implements the actual code using LangGraph's ReAct pattern
- **Input**: `TaskPlan` from Architect Agent
- **Tools Available**:
  - `write_file()`: Create/modify files with content validation
  - `read_file()`: Read existing file contents
  - `list_files()`: Browse project directory structure
  - `get_current_directory()`: Navigate file system
- **Process**: Iterates through tasks, writes code, and validates implementation

### Agent Communication Flow

```
User Prompt → Planner Agent → Plan Object
                                    ↓
                              Architect Agent → TaskPlan Object
                                                      ↓
                                                Coder Agent → Complete Project
```

## 📋 Prerequisites

- **Python 3.9+** (Python 3.10+ recommended)
- **OpenAI API Key** (recommended) - Get from [OpenAI Platform](https://platform.openai.com/api-keys) OR
- **Google Gemini API Key** (free alternative) - Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Internet Connection** (for API calls)

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
   
   Create a `.env` file in the project root with at least one of:
   
   ```env
   # Option 1: OpenAI (Recommended - GPT-4)
   OPENAI_API_KEY=sk-your-openai-key-here
   
   # Option 2: Google Gemini (Free alternative)
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   
   **Recommended Setup:**
   - Use **OpenAI GPT-4** for best results (enable web UI provider selection)
   - Use **Gemini** as free backup (no credit card required)

## 💻 Usage

### 🎨 Web Interface (Recommended)

Launch the interactive Streamlit web UI:

```bash
python main.py
# or directly
streamlit run streamlit_app.py
```

Then open http://localhost:8501 in your browser.

**Features:**
- 🚀 **Generate**: Create projects with an intuitive form
- 📂 **Browse**: View all generated projects
- 📝 **View Files**: Browse and read project files with syntax highlighting
- 📊 **Statistics**: View project statistics and file breakdowns
- 🔄 **Real-time Progress**: Track generation progress with visual feedback
- ⬇️ **Download**: Download individual files from projects

### 🖥️ CLI Mode

For headless/terminal-based interaction:

```bash
python main.py --cli
```

You'll be prompted to enter:
1. **Project prompt**: Describe what you want to build (e.g., "Create a calculator app in Python")
2. **Project name**: A folder name for your project (e.g., "calculator")

### Advanced Usage with Custom Recursion Limit

```bash
# CLI mode with custom limit
python main.py --cli --recursion-limit 150
# or short form
python main.py --cli -r 150

# Web UI mode (default)
python main.py --ui --recursion-limit 150
```

**Recursion Limit**: Controls how many agent iterations are allowed. Increase for complex projects, decrease for simpler ones (default: 100).

### Example Projects

**Example 1: Simple Calculator**
```
Enter your project prompt: Create a simple calculator in Python that can add, subtract, multiply, and divide two numbers
Enter a name for this project folder: calculator
```

**Example 2: Web Application**
```
Enter your project prompt: Build a Flask web app for a todo list with SQLite database
Enter a name for this project folder: todo-app
```

**Example 3: Game**
```
Enter your project prompt: Create a rock paper scissors game with GUI using tkinter
Enter a name for this project folder: rock-paper-scissors
```

## 📁 Project Structure

```
Multi Agent Project Generator/
├── main.py                      # Entry point (CLI + UI switcher)
├── streamlit_app.py             # 🎨 Streamlit web interface
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (API keys)
├── README.md                    # This file
├── agent/                       # Agent implementation modules
│   ├── __init__.py             # Package initialization
│   ├── graph.py                # LangGraph state machine & agent definitions
│   ├── prompts.py              # Prompt templates for each agent
│   ├── states.py               # Pydantic models for agent states
│   └── tools.py                # File system tools for coder agent
└── generated_project/          # Output directory for generated projects
    ├── calculator/             # Example generated project
    │   └── calculator.py
    └── todo-app/               # Another example
        ├── app.py
        ├── requirements.txt
        └── database.db
```

### Key Files Explained

- **`main.py`**: Entry point that launches Streamlit UI by default or CLI mode with `--cli` flag
- **`streamlit_app.py`**: Beautiful web interface for project generation, browsing, and file viewing
- **`agent/graph.py`**: Defines the LangGraph workflow connecting planner, architect, and coder agents
- **`agent/states.py`**: Pydantic models (`Plan`, `TaskPlan`, `CoderState`) for type-safe agent communication
- **`agent/prompts.py`**: Carefully crafted prompts that guide each agent's behavior
- **`agent/tools.py`**: File system tools with security (sandboxed to project directories)

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Source |
|----------|-------------|----------|--------|
| `OPENAI_API_KEY` | Your OpenAI API key (GPT-4) | Optional | [OpenAI Platform](https://platform.openai.com/api-keys) |
| `GEMINI_API_KEY` | Your Google Gemini API key | Optional | [Google AI Studio](https://makersuite.google.com/app/apikey) |

**Note:** At least one API key is required. OpenAI is recommended for better results.

### Command Line Options

| Option | Short | Mode | Description | Default |
|--------|-------|------|-------------|---------|
| `--ui` or `--streamlit` | — | Both | Launch Streamlit web UI | Default |
| `--cli` | — | Both | Run in CLI mode | — |
| `--recursion-limit` | `-r` | Both | Maximum agent iterations | 100 |

**Examples:**
```bash
python main.py                              # Launch Streamlit UI (default)
python main.py --cli                        # CLI mode
python main.py --cli -r 200                 # CLI with higher recursion
python main.py --ui -r 150                  # UI with custom recursion
```

## 🛡️ Security Features

- **Sandboxed File Operations**: All file operations are restricted to the `generated_project/<project_name>` directory
- **Path Validation**: Prevents directory traversal attacks
- **Safe Path Resolution**: Validates all file paths before operations

## 🔍 How It Works

1. **User Input**: You describe your project in natural language
2. **Planning**: Planner agent analyzes your request and creates a structured plan
3. **Architecture**: Architect agent breaks the plan into implementation tasks
4. **Implementation**: Coder agent uses tools to create files and write code
5. **Output**: Complete project is saved in `generated_project/<your-project-name>/`

### Under the Hood

- **LangGraph StateGraph**: Manages agent workflow and state transitions
- **Structured Outputs**: Ensures reliable parsing with Pydantic models
- **ReAct Pattern**: Coder agent uses reasoning and acting cycles
- **Google Gemini 2.5 Flash**: Fast, capable model for all agents

## 📦 Dependencies

- **python-dotenv**: Environment variable management
- **langchain**: LLM orchestration framework
- **langchain-google-genai**: Google Gemini integration
- **langgraph**: Graph-based agent workflows
- **pydantic**: Data validation and structured outputs

## 🐛 Troubleshooting

### Common Issues

**1. API Key Error**
```
Error: API key not found
```
**Solution**: Make sure `.env` file exists with valid `GEMINI_API_KEY`

**2. Import Error**
```
ModuleNotFoundError: No module named 'langchain'
```
**Solution**: Run `pip install -r requirements.txt`

**3. Recursion Limit Exceeded**
```
RecursionError: maximum recursion depth exceeded
```
**Solution**: Increase recursion limit with `python main.py -r 200`

**4. Empty Project Name**
```
Project name cannot be empty.
```
**Solution**: Provide a valid project folder name when prompted

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Support for more programming languages and frameworks
- Enhanced error handling and validation
- Project templates and scaffolding
- Testing framework integration
- Documentation generation
- Code review agent

## 📝 License

This project is created for **educational and research purposes**. Feel free to use, modify, and distribute as needed.

## 🎯 Future Enhancements

- [x] Web interface for easier interaction (Streamlit)
- [x] Support for multiple LLM providers (OpenAI, Gemini)
- [x] Project browser and file viewer
- [x] Real-time progress tracking
- [ ] Code quality checks and linting
- [ ] Automated testing generation
- [ ] Version control integration (auto-commit)
- [ ] Advanced project templates library
- [ ] AI code review agent
- [ ] Docker containerization support
- [ ] Project export as ZIP
- [ ] Batch project generation
- [ ] Project forking and templates
- [ ] Code documentation generation

## 🙏 Acknowledgments

- Built with [LangChain](https://www.langchain.com/) and [LangGraph](https://langchain-ai.github.io/langgraph/)
- Powered by [Google Gemini AI](https://deepmind.google/technologies/gemini/)
- Inspired by autonomous agent research and software engineering automation

## 📧 Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ by rebel47**
