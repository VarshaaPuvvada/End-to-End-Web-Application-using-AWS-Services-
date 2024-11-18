# import the JSON utility package
import json
import math  # import the Python math library for power function
import boto3  # import the AWS SDK (for Python, the package name is boto3)
from time import gmtime, strftime  # import time packages for date formatting
from decimal import Decimal  # import Decimal for DynamoDB compatibility

# create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# use the DynamoDB object to select the table
table = dynamodb.Table('CalculatorDatabase')

# store the current time in a human-readable format in a variable
now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

# define the handler function that the Lambda service will use as an entry point
def lambda_handler(event, context):
    # extract the two numbers and the operation from the Lambda service's event object
    num1 = Decimal(event['num1'])
    num2 = Decimal(event['num2'])
    operation = event['operation'].lower()

    # perform the specified operation
    if operation == 'add':
        result = num1 + num2
    elif operation == 'subtract':
        result = num1 - num2
    elif operation == 'multiply':
        result = num1 * num2
    elif operation == 'divide':
        if num2 != 0:
            result = num1 / num2
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('Error: Division by zero is not allowed')
            }
    elif operation == 'power':
        result = math.pow(num1, num2)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Unsupported operation. Use add, subtract, multiply, divide, or power.')
        }

    # write the result and time to the DynamoDB table
    response = table.put_item(
        Item={
            'ID': str(result),  # Unique identifier for the record, can use a combination of result and timestamp if needed
            'OperationType': operation,
            'Num1': num1,
            'Num2': num2,
            'Result': result,
            'LatestGreetingTime': now
        }
    )

    # return a properly formatted JSON object with the result
    return {
        'statusCode': 200,
        'body': json.dumps('Your result is ' + str(result))
    }
