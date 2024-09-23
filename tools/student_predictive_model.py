import os
import json
import shutil
import sqlite3
import boto3
from datetime import datetime
import csv
import io


def predict_student_success(course_id, student_id):
    # invoke a predictive model for a given student_id and course_id
    prediction = 1.0

    
    return prediction
     
    
def lambda_handler(event, context):   
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])
    responseBody =  {
        "TEXT": {
            "body": "Error, no function was called"
        }
    }
   
    if function == 'predict_student_success':
        course_id = None
        for param in parameters:
            if param["name"] == "course_id":
                question = param["value"]

        if not course_id:
            raise Exception("Missing mandatory parameter: course_id")
        
        student_id = None
        for param in parameters:
            if param["name"] == "student_id":
                student_id = param["value"]

        if not student_id:
            raise Exception("Missing mandatory parameter: student_id")
        
        success_rate = predict_student_success(course_id, student_id)
        
        responseBody =  {
            'TEXT': {
                "body": f"Here is the predicted success rate of {student_id} in {course_id}: {success_rate}"
            }
        }

    action_response = {
        'actionGroup': actionGroup,
        'function': function,
        'functionResponse': {
            'responseBody': responseBody
        }

    }

    function_response = {'response': action_response, 'messageVersion': event['messageVersion']}
    print("Response: {}".format(function_response))

    return function_response
