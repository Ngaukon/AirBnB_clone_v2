#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv

def setup_storage():
    """Initialize storage based on the environment variable"""
    global storage
    storage_t = getenv("HBNB_TYPE_STORAGE")
    if storage_t == "db":
        from models.engine.db_storage import DBStorage
        storage = DBStorage()
    else:
        from models.engine.file_storage import FileStorage
        storage = FileStorage()
    storage.reload()

# Call the setup function to initialize storage
setup_storage()
