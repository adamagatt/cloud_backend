import boto3
from flask import Flask
import os

def get_db_endpoint() -> str:
    return os.getenv('DB_ENDPOINT', '')

# For a Boto3 client.
ddb = boto3.client('dynamodb', 
    endpoint_url=get_db_endpoint(),
    region_name='ap-southeast-2',
    aws_access_key_id='anything',
    aws_secret_access_key='anything'
)

app = Flask(__name__)

@app.route('/')
def hello():
    return {'message': 'Hello, World!'}

@app.route('/test/')
def test_dynamodb():
    response = ddb.list_tables()
    return {'message': response['TableNames']}