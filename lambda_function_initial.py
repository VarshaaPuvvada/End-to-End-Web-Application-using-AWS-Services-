# import the JSON utility package
import json
import math  # import the Python math library for power function

# define the handler function that the Lambda service will use as an entry point
def lambda_handler(event, context):
    # extract the two numbers and the operation from the Lambda service's event object
    num1 = float(event['num1'])
    num2 = float(event['num2'])
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

    # return a properly formatted JSON object with the result
    return {
        'statusCode': 200,
        'body': json.dumps('Your result is ' + str(result))
    }

