import boto3
from flask import Flask

from .utils import initialise_tables

# For a Boto3 client.
ddb = boto3.client('dynamodb', 
    endpoint_url='http://dynamodb-local:8000',
    region_name='ap-southeast-2',
    aws_access_key_id='anything',
    aws_secret_access_key='anything'
)

initialise_tables(ddb)

app = Flask(__name__)

@app.route('/')
def hello():
    return {'message': 'Hello, World!'}

@app.route('/test/')
def test_dynamodb():
    response = ddb.list_tables()
    return {'message': response['TableNames']}