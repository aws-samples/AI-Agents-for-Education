import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random
import boto3
import matplotlib.patches as patches
import numpy as np
import os

import json
import shutil
from datetime import datetime
import csv
import io
import re

original_file = 'tools/claude_3.5_sonnet_artifacts.txt'
target_file = '/tmp/claude_3.5_sonnet_artifacts.txt'
if not os.path.exists(target_file):
    shutil.copy2(original_file, target_file)
    

def draw_fraction_rectangle(ax, total_parts, shaded_parts, position, color='pink'):
    """Draw a fraction representation using a rectangle divided into parts."""
    for i in range(total_parts):
        is_shaded = i < shaded_parts
        rect = patches.Rectangle((position[0] + i, position[1]), 1, 1, linewidth=1, 
                                 edgecolor='black', facecolor=color if is_shaded else 'white')
        ax.add_patch(rect)

def draw_fraction_circle(ax, total_parts, shaded_parts, position, color='gold'):
    """Draw a fraction representation using a circle divided into parts."""
    radius = 1
    angles = np.linspace(0, 2 * np.pi, total_parts + 1)
    for i in range(total_parts):
        is_shaded = i < shaded_parts
        wedge = patches.Wedge(position, radius, np.degrees(angles[i]), np.degrees(angles[i + 1]),
                              facecolor=color if is_shaded else 'white', edgecolor='black')
        ax.add_patch(wedge)
        
def draw_image(ax, img_path, number, x_start, y_start, scale=1.0, x_offset=None):
    """Draws images for representing numbers, with resizing and custom offsets."""
    img = mpimg.imread(img_path)
    img_height, img_width, _ = img.shape
    
    # Determine scale based on desired height in plot coordinates (e.g., 1 unit high)
    scaled_width = (img_width / img_height) * scale
    if x_offset is None:
        x_offset = scaled_width  # Ensure default offset is the width of the scaled image
    
    for i in range(number):
        ax.imshow(img, aspect='auto', extent=(x_start + i * x_offset, x_start + i * x_offset + scaled_width, y_start, y_start + scale))
    return x_start + number * x_offset  # Return the end position after the last image

def read_txt_to_string(file_path):
    with open(file_path, 'r') as file:
        txt_content = file.read()
   
    return txt_content
def generate_presigned_url(bucket_name, s3_key, expiration=3600):
    """
    Generate a pre-signed URL to share an S3 object

    :param bucket_name: string, Name of the S3 bucket
    :param object_key: string, Name of the object in the S3 bucket
    :param expiration: Time in seconds for the pre-signed URL to remain valid (default: 3600)
    :return: Pre-signed URL as string. If error, returns None.
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name, 'Key': s3_key},
                                                    ExpiresIn=expiration)
        return response
    except NoCredentialsError:
        print("Credentials not available.")
        return None
def create_svg(task):
    # call llm to handle task, to add data reading and updated prompt template
    bedrock_client = boto3.client("bedrock-runtime")
    # load artifact system prompt 
    artifact_prompt = read_txt_to_string('/tmp/claude_3.5_sonnet_artifacts.txt')

    messages = [
        {
        "role": 'user',
        "content": [ {"type": "text", "text":
f"""
Create a SVG for this task {task}. Below is how you create such an artifact.
{artifact_prompt}
"""
        }]
        }
    ]     

    body=json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": messages,
            "temperature": 0.5,
            "top_p": 1,
            "stop_sequences":["assistant"]
        }  
    ) 
    print(messages)
    
    response = bedrock_client.invoke_model(body=body, modelId="anthropic.claude-3-sonnet-20240229-v1:0")
    response_body = json.loads(response.get('body').read())
    print(response_body)
    # Extract the SVG content using a regular expression
    
    content_text = response_body['content'][0]['text']
    svg_content = re.search(r'<svg.*?>.*?</svg>', content_text, re.DOTALL).group(0)

    # Save the SVG content to a file
    file_path = f'/tmp/{task}.svg'
    with open(file_path, 'w') as file:
        file.write(svg_content)


    # Upload the file to S3
    s3 = boto3.client('s3')
    s3_bucket_name = 'sagemaker-us-east-1-827930657850'
    s3_key = f'{task}.svg'
    try:
        s3.upload_file(file_path, s3_bucket_name, s3_key)

    except Exception as e:
        print(f"Failed to upload file to S3: {e}")
    finally:
        # Clean up the local file
        if os.path.exists(file_path):
            os.remove(file_path)
            
    
    # link = f"s3://{s3_bucket_name}/{s3_key}"
    link = generate_presigned_url(s3_bucket_name, s3_key)
    print(f'SVG file {file_path} has been uploaded to {link}.')
    
    return link

def create_math_question_with_images(operation='add'):
    """
    Create a math question using images. Supports addition and subtraction.
    
    Parameters:
    - operation: Operation type, either 'add' for addition or 'subtract' for subtraction.
    """
    image_path='tools/banana.png'
    if operation == 'add':
        number_a = random.randint(1, 9)
        number_b = random.randint(1, 10 - number_a)
    elif operation == 'subtract':
        number_a = random.randint(2, 10)  # Ensure number_a is at least 2 to make subtraction possible
        number_b = random.randint(1, number_a - 1)  # Ensure number_b is less than number_a
    else:
        raise ValueError("Invalid operation. Choose either 'add' or 'subtract'.")

    total_images = number_a + number_b
    fig, ax = plt.subplots(figsize=(total_images * 1.5, 3))  # Adjust width based on total images
    ax.set_xlim(0, total_images * 1.5)  # Extend the x-axis limits
    ax.set_ylim(0, 2)
    ax.axis('off')  # Turn off the axis

    # Draw the first number
    last_x = draw_image(ax, image_path, number_a, 1, 1, scale=1)

    # Draw the operation symbol
    operation_symbol = '+' if operation == 'add' else '-'
    ax.text(last_x + 0.5, 1.5, operation_symbol, fontsize=15, ha='center')

    # Draw the second number
    next_x = draw_image(ax, image_path, number_b, last_x + 1.5, 1, scale=1)

    # Draw the equals sign
    ax.text(next_x + 0.5, 1.5, '=', fontsize=15, ha='center')

    # Draw the question mark
    ax.text(next_x + 1.5, 1.5, '?', fontsize=15, ha='center')

    # Save the plot to a temporary file
    file_path = f'/tmp/{number_a}_{operation}_{number_b}.png'
    plt.savefig(file_path)

    # Upload the file to S3
    s3 = boto3.client('s3')
    s3_bucket_name = 'mathoperation'
    s3_key = f"{number_a}_{operation}_{number_b}.png"
    try:
        s3.upload_file(file_path, s3_bucket_name, s3_key)

    except Exception as e:
        print(f"Failed to upload file to S3: {e}")
    finally:
        # Clean up the local file
        if os.path.exists(file_path):
            os.remove(file_path)
    link = f"s3://{s3_bucket_name}/{s3_key}"
    return link, number_a, number_b, operation

def create_fraction_illustration(numerator, denominator, shape ='rectangle'):
    """
    Create a fraction illustration using rectangles or circles.
    
    Parameters:
    - numerator: Number of shaded parts (top number of the fraction).
    - denominator: Total number of parts (bottom number of the fraction).
    - shape: Type of shape to use ('rectangle' or 'circle').
    """
    numerator = int(numerator)
    denominator = int(denominator)
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_xlim(-1, denominator + 1)
    ax.set_ylim(-1, 2)
    ax.axis('off')

    position = (0, 0)

    if shape == 'rectangle':
        draw_fraction_rectangle(ax, denominator, numerator, position)
    elif shape == 'circle':
        draw_fraction_circle(ax, denominator, numerator, position)
    else:
        raise ValueError("Invalid shape. Choose either 'rectangle' or 'circle'.")
 
    # Save the plot to a temporary file
    file_path = f'/tmp/{numerator}_{denominator}_{shape}.png'
    plt.savefig(file_path)


    # Upload the file to S3
    s3 = boto3.client('s3')
    s3_bucket_name = 'mathfraction'
    s3_key = f"{numerator}_{denominator}_{shape}.png"
    try:
        s3.upload_file(file_path, s3_bucket_name, s3_key)

    except Exception as e:
        print(f"Failed to upload file to S3: {e}")
    finally:
        # Clean up the local file
        if os.path.exists(file_path):
            os.remove(file_path)
    link = f"s3://{s3_bucket_name}/{s3_key}"
    return link, numerator, denominator, shape
    
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


    
    if function == 'create_math_question_with_images':
        course_code = None
        for param in parameters:
            if param["name"] == "operation":
                operation = param["value"]

        if not operation:
            raise Exception("Missing mandatory parameter: operation")
        link, number_a, number_b, operation = create_math_question_with_images(operation)
        responseBody =  {
            'TEXT': {
                "body": f"operation: {operation}, numbers: {number_a}, {number_b}, link_to_image: {link}"
            }
        }
    elif function == 'create_fraction_illustration':
        numerator = None
        denominator = None
        shape = None
        for param in parameters:
            if param["name"] == "numerator":
                numerator = param["value"]
            if param["name"] == "denominator":
                denominator = param["value"]
            if param["name"] == "shape":
                shape = param["value"] 
        if not numerator:
            raise Exception("Missing mandatory parameter: numerator")
        if not denominator:
            raise Exception("Missing mandatory parameter: denominator")

        link, numerator, denominator, shape = create_fraction_illustration(numerator, denominator, shape)
        responseBody =  {
            'TEXT': {
                "body": f"numerator/denominator: {numerator}, {denominator}, link_to_image: {link}"
            }
        }
        
    elif function == 'create_svg':
        task = None
        for param in parameters:
            if param["name"] == "task":
                task = param["value"]

        if not task:
            raise Exception("Missing mandatory parameter: task")
        
        svg_link = create_svg(task)
        
        responseBody =  {
            'TEXT': {
                "body": f"Here is the link of svg for task {task}: {svg_link}"
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
