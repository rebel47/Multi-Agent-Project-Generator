# 🚀 Quick Start Guide

Get up and running with Multi-Agent Project Generator in 5 minutes!

## Step 1: Install (2 minutes)

```bash
# Clone the repository
git clone https://github.com/rebel47/Multi-Agent-Project-Generator.git
cd Multi-Agent-Project-Generator

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Get API Key (1 minute)

Get a **FREE** API key from Google:
1. Visit https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your key

## Step 3: Configure (30 seconds)

Create a `.env` file:

```bash
# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

Or on Windows:
```powershell
"GEMINI_API_KEY=your_api_key_here" | Out-File -FilePath .env
```

## Step 4: Generate! (1 minute)

### Option A: Web UI (Easiest)

```bash
python main.py --ui
```

Open http://localhost:7860 in your browser!

### Option B: Command Line

```bash
# Use a template
python main.py --template fastapi-rest-api --name my-api

# Or describe your project
python main.py --prompt "Build a todo app with FastAPI" --name todo-app
```

## Step 5: Use Your Project

```bash
# Navigate to your project
cd generated_project/my-api

# Install dependencies
pip install -r requirements.txt

# Run your project!
python main.py
```

---

## 🎯 Quick Examples

### Example 1: REST API (30 seconds)
```bash
python main.py --template fastapi-rest-api --name my-api
```

### Example 2: React App (30 seconds)
```bash
python main.py --template react-spa --name my-app
```

### Example 3: Custom Project (1 minute)
```bash
python main.py \
  --prompt "Blog platform with markdown support" \
  --name blog \
  --review \
  --test \
  --git
```

---

## 💡 Pro Tips

1. **Start with Templates** - Faster and production-ready
2. **Enable All Features** - Add `--review --test --git --docker`
3. **Use Free Models** - Gemini and Groq are free and fast
4. **Review Generated Code** - Always check before deploying
5. **Iterate** - Use generated code as a starting point

---

## 🆘 Need Help?

- **Read the full README**: Comprehensive guide
- **Check examples**: See what others have built
- **Ask questions**: GitHub Discussions
- **Report issues**: GitHub Issues

---

## 🎉 You're Ready!

Start generating amazing projects with AI!

```bash
# Launch the web UI
python main.py --ui

# Or use the CLI
python main.py --list-templates
python main.py --template <template-name> --name <project-name>
```

Happy coding! 🚀
