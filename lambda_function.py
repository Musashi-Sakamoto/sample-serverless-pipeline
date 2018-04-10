import boto3
import json

print('Loading function')
dynamo = boto3.client('dynamodb')

def responsd(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        }
    }

def lambda_handler(event, context):
    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
        'GET': lambda dynamo, x: dynamo.scan(**x),
        'PUT': lambda dynamo, x: dynamo.update_item(**x),
    } 

    operation = event['httpMethod']
    if operation in operations:
        payload = event['queryStringParameter'] if operation == 'GET' else json.loads(event['body'])
        return responsd(None, operations[operation](dynamo, payload))
    else:
        return responsd(ValueError('Unsupported method "{}' . format(operation)))