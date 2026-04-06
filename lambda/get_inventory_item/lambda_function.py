import boto3
import json
import os

def lambda_handler(event, context):
    # DynamoDB setup
    dynamo_client = boto3.client('dynamodb')

    # Get the table name from environment variable
    table_name = os.getenv('TABLE_NAME', 'Inventory')

    # Get the key from the path parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }
    
    if 'queryStringParameters' not in event or 'location_id' not in event['queryStringParamters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'location_id' query parameter")
        }

    key_value = event['pathParameters']['id']
    location_id = int(event['queryStringParameters']['location_id'])

    # Prepare the key for DynamoDB
    key = {
        '_id': {'S': key_value},
        'location_id': {'N': str(location_id)}
    }

    # Get the item from the table
    try:
        response = dynamo_client.get_item(TableName=table_name, Key=key)
        item = response.get('Item', {})

        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps('Item not found')
            }

        return {
            'statusCode': 200,
            'body': json.dumps(item, default=str)  # Use str to handle any special types like Decimal
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }