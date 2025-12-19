# 🚀 Quick Start Guide - Multi-Agent Project Generator

## 📋 Prerequisites

- Python 3.9+
- OpenAI API Key OR Google Gemini API Key
- 5 minutes of your time

## ⚡ 30-Second Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file with your API key
echo "OPENAI_API_KEY=sk-your-key-here" > .env
# OR
echo "GEMINI_API_KEY=your-gemini-key" > .env

# 3. Launch the web UI
python main.py
# Opens at http://localhost:8501
```

## 🎯 Using the Web Interface

### Generate a Project (2 minutes)
1. Go to the **"🚀 Generate"** tab
2. Enter a project name (e.g., `my-calculator`)
3. Describe what you want (e.g., "Create a calculator app in Python with add, subtract, multiply, divide")
4. Click **"🚀 Generate Project"**
5. Watch the progress bar as agents work
6. ✅ Project created!

### View Your Projects (1 minute)
1. Go to the **"📂 Browse Projects"** tab
2. Select your project from the dropdown
3. Choose between:
   - **📂 Structure**: View project file tree
   - **📝 Files**: Browse and read code files
   - **📊 Stats**: See project statistics

### Download Files
- Click **"⬇️ Download File"** to save individual files

## 💻 Using the CLI (Alternative)

```bash
# Interactive mode
python main.py --cli

# With custom recursion limit
python main.py --cli -r 150
```

## 🔑 Getting API Keys

### OpenAI (Recommended - $0.01/request)
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy and paste into `.env`
4. Uses GPT-4 by default

### Google Gemini (Free Alternative)
1. Go to https://makersuite.google.com/app/apikey
2. Create new API key
3. Copy and paste into `.env`
4. No credit card required!

## 📂 Project Output

Your generated projects are saved in:
```
generated_project/
├── my-calculator/
│   ├── calculator.py
│   └── requirements.txt
├── todo-app/
│   ├── app.py
│   ├── database.db
│   └── requirements.txt
└── ...
```

## 🎓 Example Prompts

### Python Calculator
```
Create a Python calculator that can add, subtract, multiply, and divide two numbers. 
Include error handling for division by zero.
```

### Web Todo App
```
Build a Flask web application for a todo list with:
- SQLite database
- Add/delete/edit tasks
- Mark tasks as complete
- Bootstrap styling
```

### Game
```
Create a Rock Paper Scissors game in Python with:
- Command-line interface
- Player vs Computer
- Score tracking
- Best of 5 rounds
```

### Frontend
```
Build a React dashboard that displays real-time charts using Recharts library.
Include temperature and humidity data visualizations.
```

## ⚙️ Configuration

### Environment Variables
```env
OPENAI_API_KEY=sk-your-openai-key          # (Recommended)
GEMINI_API_KEY=your-gemini-key             # (Optional fallback)
```

### Command Options
```bash
python main.py                              # Launch UI (default)
python main.py --ui                         # Explicit UI mode
python main.py --cli                        # CLI mode
python main.py --cli -r 200                 # Custom recursion limit
```

## 🐛 Troubleshooting

### "No LLM API key found"
**Solution:** Add `OPENAI_API_KEY` or `GEMINI_API_KEY` to `.env`

### "Streamlit not found"
**Solution:** Run `pip install -r requirements.txt`

### App takes too long
**Solution:** Use `--recursion-limit 50` for simpler projects

### Port 8501 already in use
**Solution:** Streamlit will automatically use 8502, 8503, etc.

## 📚 Next Steps

- ✅ Generate your first project
- 🔍 Browse the generated files
- 🚀 Run the generated code
- 📝 Customize and improve it
- 🎯 Use it as a template

## 💡 Pro Tips

1. **Be specific** in your prompts - more details = better code
2. **Check generated files** before running
3. **Use OpenAI** for complex projects (better quality)
4. **Use Gemini** for quick prototypes (free!)
5. **Increase recursion limit** for larger projects

## 🆘 Need Help?

- Check the [README.md](README.md) for full documentation
- Report issues on [GitHub](https://github.com/rebel47/Multi-Agent-Project-Generator/issues)
- Review generated projects for best practices

---

**Ready to generate your first project?** 🎉

```bash
python main.py
```

Then describe what you want to build!
