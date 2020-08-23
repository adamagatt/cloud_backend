import boto3
from flask import Flask, abort, request
from hashids import Hashids
from random import randint
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
ddb = boto3.resource('dynamodb', **ddb_keyargs)
player_table = ddb.Table('Player')

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

    player_id = Hashids(salt=HASH_SALT).encode(randint(1, 1_000_000))
    start_location = {
        'x': str(randint(0, 10)),
        'y': str(randint(0, 10))
    }
    try: 
        player_table.put_item(
            Item={
                'ID': player_id,
                'name': player_name,
                'location': start_location
            }
        )
    except Exception as e:
        print(e)
    return {
        'player_created': True,
        'player_id': player_id
    }

@app.route('/player/<id>')
def get_player(id):
    if id is None:
        abort(400, {"error": "Must supply a player ID"})
    else:
        result = player_table.get_item(
            Key={
                'ID': str(id)
            }
        )
        if 'Item' not in result:
            abort(404)
        else:
            record = result['Item']
            return record

