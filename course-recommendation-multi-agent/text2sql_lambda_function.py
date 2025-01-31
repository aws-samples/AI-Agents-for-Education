import json
import sqlite3
import os
import shutil
from datetime import datetime

original_db_file = 'porterville_academic.db'
target_db_file = '/tmp/porterville_academic.db'
if not os.path.exists(target_db_file):
    shutil.copy2(original_db_file, target_db_file)
        
def lambda_handler(event, context):
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])
    body_text=''
    if function == 'get_schema':
        body_text="""
Table Name 'student_schedule':
(Column Name, 'student_id', 'TEXT')
(Column Name, 'term', 'INTEGER')
(Column Name, 'course_code', 'TEXT')
(Column Name, 'print_daytime', 'TEXT')
(Column Name, 'building_number', 'TEXT')
(Column Name, 'room_number', 'TEXT')
(Column Name, 'class_days', 'TEXT')
(Column Name, 'class_start_time', 'REAL')
(Column Name, 'class_end_time', 'REAL')

<examples>
Question: Show me the class days for student testuserb to take the BIOE221 course.
Query: SELECT class_days FROM student_schedule
WHERE student_id = 'testuserb' AND course_code = 'BIOE221';
</examples>

--------------------------------------------------------

Table Name 'course_schedule':
(Column Name, 'term', 'INTEGER')
(Column Name, 'course_code', 'TEXT')
(Column Name, 'print_daytime', 'TEXT')
(Column Name, 'building_number', 'TEXT')
(Column Name, 'room_number', 'TEXT')
(Column Name, 'class_days', 'TEXT')
(Column Name, 'class_start_time', 'REAL')
(Column Name, 'class_end_time', 'REAL')

--------------------------------------------------------

Table Name 'student_data':
(Column Name, 'student_id', 'INTEGER')
(Column Name, 'term', 'INTEGER')
(Column Name, 'course_code', 'TEXT')
(Column Name, 'credits', 'REAL')
(Column Name, 'grade', 'TEXT')
(Column Name, 'major', 'TEXT')

<query-principle>
1. Don't make up column names.
</query-principle>
"""
    elif function == 'sql_validation':
        query = None
        for param in parameters:
            if param["name"] == "query":
                query = param["value"]

        if not query:
            raise Exception("Missing mandatory parameter: query")
        # Connect to the SQLite database
        print(query)  
        
#         # filtering logic
#         if not student_id:
            
#         if 'student_data' in query:
#             if 'where' in query or 'WHERE' in query:
#                 query += f' and student_id={student_id}'
#             else
#                 query += f' where student_id={student_id}'
        
        conn = sqlite3.connect('/tmp/porterville_academic.db')

        # Create a cursor object
        cursor = conn.cursor()

        # Execute the query
        try:
            cursor.execute(query)
            # Fetch all results
            rows = cursor.fetchall()
        except sqlite3.OperationalError as e:
        # Handle operational errors (e.g., syntax errors, missing tables)
            rows = str(e)
        except sqlite3.IntegrityError as e:
        # Handle integrity errors (e.g., constraint violations)
            rows = str(e)
        except Exception as e:
        # Handle any other exceptions
            rows = str(e)

        # Close the connection
        conn.close()
    
        body_text=str(rows) 
    else:
        pass

    # Execute your business logic here. For more information, refer to: https://docs.aws.amazon.com/bedrock/latest/userguide/agents-lambda.html
    responseBody =  {
        "TEXT": {
            "body": body_text
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
