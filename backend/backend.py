import boto3
from flask import Flask, abort, request
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
        'x': {'N': uniform(0, 10)},
        'y': {'N': uniform(0, 10)}
    }
    response = ddb.put_item(
        TableName='Player',
        Item={
            'ID': {'S': player_id},
            'name': {'S': player_name},
            'location': {'M': start_location}
        }
    )
    return response

@app.route('/player/<id>')
def get_player(id):
    if id is None:
        abort(400, {"error": "Must supply a player ID"})
    else:
        return ddb.get_item(
            TableName='Player',
            Key={
                'ID': id
            }
        ) 