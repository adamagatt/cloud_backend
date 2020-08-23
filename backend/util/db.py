import boto3
from typing import Dict

from .settings import get_db_endpoint, is_local

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

def list_tables():
    return ddb.list_tables()

def put_player_in_db(id: str, name: str, start_location: Dict[str, str]) -> None:
    player_table.put_item(
        Item={
            'ID': id,
            'name': name,
            'location': start_location
        }
    )

def get_player_from_db(id: str):
    result = player_table.get_item(
            Key={
                'ID': str(id)
            }
        )
    return (result.get('Item'))