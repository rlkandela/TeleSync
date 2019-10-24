# coding: utf-8
"""File for loading the local configuration"""
import os

# DEBUG
SYNC_INSTALLATION_FOLDER = "/home/rlkandela/Documents/TeleSync/"
# DEBUG
# SYNC_INSTALLATION_FOLDER = "/usr/local/bin/TeleSync/"

SYNC_CONFIG_DIR = "/home/"+os.environ['USER']+"/.config/TeleSync/"
SYNC_CONFIG_FILE = SYNC_CONFIG_DIR+"sync.conf"

def get_synchronized_folders():
    """Returns a list of the folders and files synchronized"""
    if not os.path.isdir(SYNC_CONFIG_DIR):
        os.mkdir(SYNC_CONFIG_DIR, 0o755)

    if not os.path.isfile(SYNC_CONFIG_FILE):
        with open(SYNC_CONFIG_FILE, "w") as f:
            f.close()

    with open(SYNC_CONFIG_FILE, "r") as f:
        folders = f.readlines()

        ret = []
        for folder in folders:
            ret.append(folder.rsplit("\n")[0])
        f.close()
        return ret
