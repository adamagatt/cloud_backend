from os import environ, getenv
from typing import Optional

def is_local() -> bool:
    return 'LOCAL_DB_ENDPOINT' in environ

def get_db_endpoint() -> Optional[str]:
    return getenv('LOCAL_DB_ENDPOINT', '')