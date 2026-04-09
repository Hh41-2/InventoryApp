import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from decimal import Decimal


# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Define the DynamoDB table name
TABLE_NAME = 'Inventory'

# Function to convert Decimal to int/float
def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):  
        return int(obj) if obj % 1 == 0 else float(obj)  # Convert to int if whole number, else float
    return obj

def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)
    pK = event['pathParameters']['id']

    try:
        response = table.query(
            KeyConditionExpression=Key('_id').eq(pK)
        )
        items = response.get('Items', [])

        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps(f"Item with ID {pK} not found.")
            }

        items = convert_decimals(items)
        location_id = items[0]['location_id']

        table.delete_item(Key = {'_id':pK, 'location_id':location_id})
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {pK} deleted successfully.")
        }

    except ClientError as e:
        print(f"Failed to delete inventory items: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Failed to delete inventory items: {e.response['Error']['Message']}")
        }
