import boto3
from flask import Flask, abort, request
import os

from .util.db import list_tables
from .util.player import get_player, register_player

def is_local() -> bool:
    return 'LOCAL_DB_ENDPOINT' in os.environ

app = Flask(__name__)

@app.route('/')
def hello():
    return {'message': 'Hello, World!'}

@app.route('/test/')
def test_dynamodb():
    return {'message': list_tables()}

@app.route('/player/', methods=['POST'])
def post_player_handler():
    player_name = request.form.get('name', 'Anonymous')

    player_id = register_player(player_name)

    if player_id is None:
        return {
            'player_created': False,
            'player_id': None
        }
    else:
        return {
            'player_created': True,
            'player_id': player_id
        }

@app.route('/player/<id>')
def get_player_handler(id):
    if id is None:
        abort(400, {"error": "Must supply a player ID"})
    else:
        if (player := get_player(id)) is None:
            abort(404)
        else:
            return player
