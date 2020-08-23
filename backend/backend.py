import boto3
from flask import Flask, request
from hashids import Hashids
from random import uniform
from typing import Optional
import os

HASH_SALT: str = 'webdungeon'

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
ddb = boto3.client('dynamodb', **ddb_keyargs)

app = Flask(__name__)

@app.route('/')
def hello():
    return {'message': 'Hello, World!'}

@app.route('/test/')
def test_dynamodb():
    response = ddb.list_tables()
    return {'message': response['TableNames']}

@app.route('/player/', methods=['POST'])
def register_player():
    player_name = request.form.get('name', 'Anonymous')

    player_id = Hashids(salt=HASH_SALT).encode(uniform(1, 1_000_000))
    start_location = {
        'x': uniform(0, 10),
        'y': uniform(0, 10)
    }
    response = ddb.put_item(
        TableName='Player',
        Item={
            'ID': player_id,
            'name': player_name,
            'location': start_location
        }
    )
    return response