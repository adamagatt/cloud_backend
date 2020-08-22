import boto3
from flask import Flask
import json
from typing import Optional
import os

def is_local() -> bool:
    return 'LOCAL_DB_ENDPOINT' in os.environ

def get_db_endpoint() -> Optional[str]:
    return os.getenv('LOCAL_DB_ENDPOINT', '')

# For a Boto3 client.
ddb_keyargs = ({
    'endpoint_url': get_db_endpoint(),
    'region_name': 'ap-southeast-2',
    'aws_access_key_id': 'anything',
    'aws_secret_access_key': 'anything'
} if is_local() else {
    'region_name': 'ap-southeast-2',
})

app = Flask(__name__)

@app.route('/')
def hello():
    return {'message': 'Hello, World!'}

@app.route('/test/')
def test_dynamodb():
    ddb = boto3.client('dynamodb', **ddb_keyargs)
    return {'message': json.dumps(ddb)}
    #response = ddb.list_tables()
    #return {'message': response['TableNames']}