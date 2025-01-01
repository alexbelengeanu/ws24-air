from pymilvus import MilvusClient
import os

def create_local_db(db_name='local.db', remove_if_exists = False):
    if remove_if_exists:
        if os.path.exists(db_name):
            os.remove(db_name)
        if os.path.exists(f".{db_name}.lock"):
            os.remove(f".{db_name}.lock")

    client = MilvusClient(db_name)
    return client