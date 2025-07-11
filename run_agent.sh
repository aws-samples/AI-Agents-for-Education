#!/bin/bash

# Course Recommendation Agent Runner Script
# This script automatically handles virtual environment setup and runs the agent

echo "🚀 Starting Course Recommendation Agent..."

# Change to the strands-implementation directory
cd "$(dirname "$0")/strands-implementation"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
    
    echo "📥 Installing required packages..."
    pip install -r requirements-strands.txt
else
    echo "🔧 Activating existing virtual environment..."
    source venv/bin/activate
fi

# Run the agent
echo "▶️  Running agent..."
echo "============================================================"
python agent.py

echo "👋 Agent session ended."
