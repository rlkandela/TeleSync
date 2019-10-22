
"""File containing methods to read api_id and api_hash"""

# File where the telegram app id is saved
ID_FILE = "../config/id_file.conf"

# File where the telegram app hash is saved
HASH_FILE = "../config/hash_file.conf"

def get_api_id():
    """Method to read api_id from ID_FILE"""
    with open(ID_FILE, "r") as f:
        api_id = f.readline()
        f.close()
    return api_id

def get_hash_id():
    """Method to read api_hash from HASH_FILE"""
    with open(HASH_FILE, "r") as f:
        api_hash = f.readline()
        f.close()
    return api_hash
