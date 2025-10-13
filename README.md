# Multi Agent Project Generator

This project is a multi-agent system that generates complete engineering projects based on user prompts. It uses Gemini AI and LangGraph to plan, architect, and code projects automatically.

## Features
- Converts user prompts into structured project plans
- Breaks down plans into explicit engineering tasks
- Generates code and files for each project in a separate folder
- Supports multiple tech stacks and project types

## How to Use

1. Make sure you have Python installed (version 3.7+ recommended).
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set your Gemini API key in a `.env` file:
   ```
   GEMINI_API_KEY=your_key_here
   ```
4. Run the main program:
   ```
   python main.py
   ```
5. Enter your project prompt and a name for the project folder when prompted.

## Project Structure
- `main.py` : Entry point for the multi-agent generator
- `agent/` : Contains agent logic, prompts, states, and tools
- `generated_project/` : Folder where generated projects are stored
- `.env` : Environment variables (API keys)

## License
This project is generated for educational and research purposes.
