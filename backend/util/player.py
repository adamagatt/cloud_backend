from hashids import Hashids
from random import randint
from typing import Optional

from .db import get_player_from_db, put_player_in_db

hashids = Hashids(salt='webdungeon')

def register_player(name: str) -> Optional[str]:
    player_id = hashids.encode(randint(1, 1_000_000))
    start_location = {
        'x': str(randint(0, 10)),
        'y': str(randint(0, 10))
    }
    try:
        put_player_in_db(player_id, name, start_location)
    except Exception as e:
        print(e)
        return None

    return player_id

def get_player(id: str):
    return get_player_from_db(id)