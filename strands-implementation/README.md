# Course Recommendation Agent - Strands Implementation

A streamlined implementation of the Course Recommendation Agent using the Strands Agents SDK.

## 🚀 Quick Start

1. **Run the data preparation notebook:**
   ```bash
   jupyter notebook ../data-prep-course-recommendation-agent-short.ipynb
   ```

2. **Install dependencies and run:**
   ```bash
   pip install -r requirements-strands.txt
   python agent.py
   ```

**Alternative: Setup with testing:**
```bash
python setup_strands_agent.py  # Install deps, run tests, then start agent
```

That's it! The agent automatically uses the knowledge base created by the notebook.

## 📁 Files

| File | Purpose |
|------|---------|
| `agent.py` | **Main script** - Run this for interactive chat |
| `tools.py` | Tool functions (SQL, predictions) |
| `setup_strands_agent.py` | **Setup & testing** - Dependencies, tests, validation |
| `requirements-strands.txt` | Dependencies |

## ✨ Features

- Real course catalog data from Bedrock Knowledge Base (via Strands retrieve)
- SQL queries against student/course database  

## 🎯 Sample Questions

- "How many credits has student 1 earned?"
- "What courses are offered this semester for biology majors?"

## 🔧 Requirements

- Python 3.8+
- AWS credentials (for Bedrock)
- Data prep notebook completed


