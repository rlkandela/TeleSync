# coding: utf-8
"""File for loading the local configuration"""
import os

# DEBUG
SYNC_INSTALLATION_FOLDER = "/home/rlkandela/Documents/TeleSync/TeleSync/"
"""Path to the installation folder DEBUG version"""

# DEBUG
# SYNC_INSTALLATION_FOLDER = "/opt/TeleSync/"
#"""Path to the installation folder"""

### Main program must make sure that its not running as root and ask after it for root password
SYNC_CONFIG_DIR = "/home/"+os.environ['USER']+"/.config/TeleSync/"
"""Path to the config directory"""

SYNC_CONFIG_FILE = SYNC_CONFIG_DIR+"sync.conf"
"""Path to the config file"""

MAX_DIR_SIZE = 300
"""Maximum size in bytes a folder can weight"""

TMP_FOLDER = "/tmp/TeleSync/"
"""Path to the temporary folder"""

def check_config_elements():
    """Function that checks if the config folder and file exists and in case they don't it creates them"""

    if not os.path.isdir(SYNC_CONFIG_DIR):
        os.mkdir(SYNC_CONFIG_DIR, 0o755)

    if not os.path.isfile(SYNC_CONFIG_FILE):
        with open(SYNC_CONFIG_FILE, "w") as f:
            f.close()

def get_synchronized_items():
    """Returns a list of the folders and files synchronized

    Returns:
        list of str: List of items configured for synchronization
    """

    check_config_elements()

    with open(SYNC_CONFIG_FILE, "r") as f:
        items = f.readlines()

        ret = []
        for item in items:
            ret.append(item.rsplit("\n")[0])
        f.close()
        return ret
