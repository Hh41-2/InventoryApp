import boto3
from boto3.dynamodb.conditions import Key
import json
import os

def lambda_handler(event, context):
    # Initialize a DynamoDB client
    dynamo_client = boto3.resource('dynamodb')

    # Get the table name from environment variable
    table_name = os.getenv('TABLE_NAME', 'Inventory')
    
    inventoryTable = dynamo_client.Table(table_name)

    # Extract the '_id' from the path parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }
    
    location_id = int(event['pathParameters']['id'])

    # Scan the table
    try:
        response = inventoryTable.query(
            IndexName = 'GSI_SK_PK',  # Your GSI name
            KeyConditionExpression=Key('location_id').eq(location_id) 
        )
        items = response['Items']

        return {
            'statusCode': 200,
            'body': json.dumps(items, default=str)  
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }