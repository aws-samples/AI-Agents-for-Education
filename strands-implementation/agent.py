#!/usr/bin/env python3
"""
Course Recommendation Agent

This module contains the main agent logic and configuration.
"""

import logging
import os

from strands import Agent
from strands_tools import retrieve

from custom_tools import (
    get_schema, 
    sql_query, 
    predict_student_success,
    setup_knowledge_base_env
)

# Configure logging
logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Agent instruction
AGENT_INSTRUCTION = """
You are an AI agent to recommend courses to maximize student success and fulfill program requirements.

Resources:
1. Database Tables:
   - student_data: Academic history and progress
   - student_schedule: Current course enrollments
   - course_schedule: Upcoming course offerings
2. Knowledge Base:
   - Course catalog with descriptions and prerequisites from 2024-2025 Porterville College Catalog
   - Program requirements for majors and minors (automatically configured from data-prep notebook)
3. Tools:
   - get_schema: Get database schema information
   - sql_query: Execute SQL queries against student and course data
   - predict_student_success: Forecast student performance in courses

Recommendation Process:
1. Retrieve Student Data:
   - Use SQL to gather academic history and current courses
2. Identify Suitable Courses:
   - Match available courses with unmet program requirements
3. Evaluate and Recommend:
   - Predict success using the predictive tool
   - Recommend courses that align with strengths and program needs
4. Explain Decision:
   - Provide a clear rationale for recommendations based on prerequisites, relevance, and predicted success

When using the retrieve tool, pass the user's question as-is without modification to get the most relevant results from the knowledge base.

If you are not asked of recommendation related tasks, you don't have to follow the recommendation process, but leverage the information you have access to.
Assist only with academic-related queries.
"""

def create_agent():
    """Create and return the course recommendation agent."""
    agent = Agent(
        system_prompt=AGENT_INSTRUCTION,
        tools=[
            get_schema,
            sql_query,
            predict_student_success,
            retrieve  # Native Strands retrieve tool
        ],
        # Using Claude 4 Sonnet as the default model (via Bedrock)
        model="us.anthropic.claude-3-5-haiku-20241022-v1:0",
        # Supress agent orchestration messages
        callback_handler=None
    )
    return agent

def interactive_session(agent):
    """
    Run an interactive session with the course recommendation agent.
    Type 'quit' to exit.
    """
    print("\n" + "=" * 60)
    print("COURSE RECOMMENDATION AGENT - INTERACTIVE MODE")
    print("Using Real Knowledge Base from 2024-2025 Catalog")
    print("=" * 60)
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("\nAgent: ", end="")
            response = agent(user_input)
            print(response)
            print("\n" + "-" * 50 + "\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again.\n")

def main():
    """Main function to run the course recommendation agent."""
    print("Initializing Course Recommendation Agent...")
    
    # Setup knowledge base environment
    kb_configured = setup_knowledge_base_env()
    if kb_configured:
        print(f"✅ Using Bedrock Knowledge Base: {os.environ.get('KNOWLEDGE_BASE_ID')}")
    else:
        print("⚠️  No Knowledge Base configured.")
        print("Please run the data-prep notebook to create and configure the knowledge base:")
        print("jupyter notebook ../data-prep-course-recommendation-agent-short.ipynb")
    
    try:
        # Create the agent
        agent = create_agent()
        print("Course Recommendation Agent created successfully!")
        print(f"Model: {agent.model.config}")
        
        # Start interactive session
        interactive_session(agent)
        
    except Exception as e:
        print(f"Error initializing agent: {str(e)}")
        print("Please ensure you have:")
        print("1. Installed strands-agents: pip install strands-agents")
        print("2. Configured AWS credentials for Bedrock access")
        print("3. Prepared the database using the data preparation notebook")

if __name__ == "__main__":
    main()
