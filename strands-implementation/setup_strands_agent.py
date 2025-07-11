#!/usr/bin/env python3
"""
Setup and Test script for the Strands Course Recommendation Agent

This script installs dependencies, checks requirements, and runs tests.
"""

import subprocess
import sys
import os
from tools import (
    get_schema,
    sql_query,
    predict_student_success,
    setup_knowledge_base_env
)

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required Python packages."""
    print("🔄 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-strands.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    except FileNotFoundError:
        print("❌ requirements-strands.txt not found")
        return False

def test_imports():
    """Test if required packages can be imported."""
    print("🔄 Testing imports...")
    try:
        from strands import Agent
        from strands_tools import retrieve
        import boto3
        print("✅ All required packages imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def check_prerequisites():
    """Check if data prep has been run."""
    db_file = "../porterville_academic.db"
    if not os.path.exists(db_file):
        print("⚠️  Database not found. Please run the data preparation notebook first:")
        print("   jupyter notebook ../data-prep-course-recommendation-agent-short.ipynb")
        return False
    
    config_file = "kb_config.json"
    if not os.path.exists(config_file):
        print("⚠️  Knowledge base config not found. Please complete the data preparation notebook.")
        return False
    
    print("✅ Prerequisites met")
    return True

def test_tools_directly():
    """Test individual tools directly for debugging purposes."""
    print("\n" + "=" * 60)
    print("DIRECT TOOL TESTING")
    print("=" * 60)
    
    # Test schema tool
    print("1. Schema Tool:")
    try:
        schema_result = get_schema()
        print(schema_result[:200] + "...")
    except Exception as e:
        print(f"Error: {e}")
    print()
    
    # Test SQL query tool
    print("2. SQL Query Tool:")
    try:
        sql_result = sql_query("SELECT student_id, major FROM student_data LIMIT 3")
        print(sql_result)
    except Exception as e:
        print(f"Error: {e}")
    print()
    
    # Test prediction tool
    print("3. Prediction Tool:")
    try:
        prediction_result = predict_student_success(course_id="BIOL P110", student_id="1")
        print(prediction_result)
    except Exception as e:
        print(f"Error: {e}")
    print()
    
    # Note about retrieve tool
    print("4. Retrieve Tool:")
    print("The native Strands retrieve tool is available to the agent.")
    print("It will be used automatically when the agent needs knowledge base information.")
    print("Environment configured:", "KNOWLEDGE_BASE_ID" in os.environ)

def run_agent_tests():
    """Run a series of test queries against the agent."""
    print("\n" + "=" * 60)
    print("RUNNING AGENT TESTS WITH REAL KNOWLEDGE BASE")
    print("=" * 60)
    
    try:
        from agent import create_agent
        agent = create_agent()
        
        test_queries = [
            "How many credits has student 1 earned?",
            "What courses are offered this semester (202408) that are relevant to a biology major?",
            "Does the course BIOL P110 conflict with student 1's current schedule?",
            "What are the prerequisites for BIOL P110?",
            "Tell me about the Biology program requirements at Porterville College.",
            "What courses do you recommend for student 1 to take this semester (202408)? Please consider their academic history, major requirements, and predicted success rates."
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n=== Test {i}: {query[:50]}{'...' if len(query) > 50 else ''} ===")
            try:
                response = agent(query)
                print(response)
            except Exception as e:
                print(f"Error: {str(e)}")
            print("\n" + "-" * 50)
            
    except Exception as e:
        print(f"❌ Failed to run agent tests: {e}")
        return False
    
    return True

def main():
    """Main setup and test function."""
    print("=" * 50)
    print("🚀 STRANDS AGENT SETUP & TEST")
    print("=" * 50)
    
    steps = [
        ("Python Version", check_python_version),
        ("Install Dependencies", install_dependencies),
        ("Test Imports", test_imports),
        ("Check Prerequisites", check_prerequisites),
    ]
    
    all_passed = True
    for name, func in steps:
        print(f"\n📋 {name}")
        if not func():
            all_passed = False
    
    if all_passed:
        # Setup knowledge base environment
        print(f"\n📋 Knowledge Base Setup")
        kb_configured = setup_knowledge_base_env()
        
        if kb_configured:
            print(f"✅ Knowledge Base configured: {os.environ.get('KNOWLEDGE_BASE_ID')}")
            
            # Run tests
            test_tools_directly()
            
            # Ask if user wants to run full agent tests
            print("\n" + "=" * 50)
            run_tests = input("Run full agent tests? (y/n): ").strip().lower()
            if run_tests in ['y', 'yes']:
                run_agent_tests()
            
            print("\n" + "=" * 50)
            print("🎉 Setup complete! You can now run:")
            print("   python agent.py")
        else:
            print("⚠️  Knowledge base not configured. Please run the data-prep notebook first.")
    else:
        print("\n⚠️  Please resolve the issues above")

if __name__ == "__main__":
    main()
