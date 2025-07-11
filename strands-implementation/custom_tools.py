#!/usr/bin/env python3
"""
Tools for Course Recommendation Agent - Direct Function Calls

This module directly calls the existing function implementations from tools directory
"""

from strands import tool
import sys
import os
import json
import logging

# Add the tools directory to Python path to import the existing function
tools_path = os.path.join(os.path.dirname(__file__), '..', 'tools')
sys.path.insert(0, tools_path)

from text2sql_lambda_function_porterville import lambda_handler

# Import the lambda_handler from student_predictive_model.py
from student_predictive_model import lambda_handler as student_prediction_handler

# Configure logging
logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def call_existing_function(function_name: str, parameters: list = None) -> str:
    """
    Call the existing Lambda function implementation directly.
    
    Args:
        function_name: The function to call ('get_schema' or 'sql_query')
        parameters: List of parameters for the function
        
    Returns:
        Response from the function
    """
    try:
        # Construct event matching your existing Lambda structure
        event = {
            'agent': 'course-recommendation-agent',
            'actionGroup': 'database-tools',
            'function': function_name,
            'messageVersion': '1.0'
        }
        
        if parameters:
            event['parameters'] = parameters
        
        # Call the existing lambda_handler function directly
        result = lambda_handler(event, None)
        
        # Extract the body text from the response structure
        if 'response' in result and 'functionResponse' in result['response']:
            response_body = result['response']['functionResponse']['responseBody']
            if 'TEXT' in response_body and 'body' in response_body['TEXT']:
                return response_body['TEXT']['body']
        
        return f"Unexpected response format: {result}"
        
    except Exception as e:
        logger.error(f"Error calling function {function_name}: {str(e)}")
        return f"Error calling function: {str(e)}"

@tool
def get_schema() -> str:
    """Get the database schema for all tables."""
    return call_existing_function('get_schema')

@tool
def sql_query(query: str) -> str:
    """
    Execute a SQL query against the academic database.
    
    Args:
        query: SQL query string to execute
        
    Returns:
        Query results as a string
    """
    if not query:
        return "Error: Missing mandatory parameter: query"
    
    parameters = [{"name": "query", "value": query}]
    return call_existing_function('sql_query', parameters)

@tool
def predict_student_success(course_id: str, student_id: str) -> str:
    """
    Predict the success rate of a student taking a specific course.
    
    Args:
        course_id: The course identifier
        student_id: The student identifier
        
    Returns:
        Predicted success rate and explanation
    """
    if not course_id or not student_id:
        return "Error: Both course_id and student_id are required parameters."
    
    try:
        # Create event structure for the Lambda function
        event = {
            'agent': 'course-recommendation-agent',
            'actionGroup': 'student-prediction',
            'function': 'predict_student_success',
            'messageVersion': '1.0',
            'parameters': [
                {'name': 'course_id', 'value': course_id},
                {'name': 'student_id', 'value': student_id}
            ]
        }
        
        # Call the Lambda handler directly
        response = student_prediction_handler(event, {})
        
        # Extract the response body
        return response['response']['functionResponse']['responseBody']['TEXT']['body']
    except Exception as e:
        return f"Error predicting student success: {str(e)}"

def setup_knowledge_base_env():
    """Set up environment variables for the Strands retrieve tool."""
    config_file = '../kb_config.json'
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                kb_id = config.get('knowledge_base_id')
                if kb_id:
                    os.environ["KNOWLEDGE_BASE_ID"] = kb_id
                    os.environ["AWS_REGION"] = os.environ.get("AWS_REGION", "us-east-1")
                    os.environ["MIN_SCORE"] = "0.4"
                    logger.info(f"Knowledge Base configured: {kb_id}")
                    return True
        except Exception as e:
            logger.warning(f"Error reading config file: {e}")
    
    logger.warning("No Knowledge Base ID found. Please run the data-prep notebook.")
    return False
