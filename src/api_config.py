# coding: utf-8
"""File containing methods to read api_id and api_hash, also contains the name of the channel"""

ID_FILE = "../config/id_file.conf"
"""File where the telegram app id is saved"""

HASH_FILE = "../config/hash_file.conf"
"""File where the telegram app hash is saved"""

CHANNEL_NAME = "TeleSync"
"""Name of the telegram channel where the files will be uploaded"""

def get_api_id():
    """Method to read api_id from ID_FILE

    Returns:
        str: The value of the API id
    """
    with open(ID_FILE, "r") as f:
        api_id = f.readline()
        api_id = api_id.rsplit("\n")[0]
        f.close()
    return api_id

def get_hash_id():
    """Method to read api_hash from HASH_FILE

    Returns:
        str: The value of the API hash
    """
    with open(HASH_FILE, "r") as f:
        api_hash = f.readline()
        api_hash = api_hash.rstrip("\n")
        f.close()
    return api_hash
