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

    # Scan the table
    try:
        response = inventoryTable.query(
            IndexName = 'GSI_SK_PK',  # Your GSI name
            KeyConditionExpression=Key('location_id').eq('1') 
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