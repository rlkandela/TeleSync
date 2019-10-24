# coding: utf-8
"""File for configuring the installation"""
import os
from telethon import TelegramClient
import system_config
import api_config

def save_api_id():
    """Function for saving the app id on $(INSTALLATION_FOLDER)/config/id_file.conf"""
    if not os.path.isdir(system_config.SYNC_INSTALLATION_FOLDER+"config/"):
        os.mkdir(system_config.SYNC_INSTALLATION_FOLDER+"config/", 0o755)

    if not os.path.isfile(system_config.SYNC_INSTALLATION_FOLDER+"config/id_file.conf"):
        try:
            with open(system_config.SYNC_INSTALLATION_FOLDER+"config/id_file.conf", "w") as f:
                api_id = int(input("Enter the app id: "))
                f.write(str(api_id))
                f.close()
        except ValueError:
            print("The ID is in an incorrect format")
        except IOError:
            print("Could not create or modify the file")
    else:
        if input("There is already an id saved, do you want to rewrite it? y/N ") == "y":
            try:
                with open(system_config.SYNC_INSTALLATION_FOLDER+"config/id_file.conf", "w") as f:
                    api_id = int(input("Enter the app id: "))
                    f.write(str(api_id))
                    f.close()
            except ValueError:
                print("The ID is in an incorrect format")
            except IOError:
                print("Could not create or modify the file")
        else:
            print("API ID not changed")


def save_api_hash():
    """Function for saving the app hash on $(INSTALLATION_FOLDER)/config/hash_file.conf"""
    if not os.path.isdir(system_config.SYNC_INSTALLATION_FOLDER+"config/"):
        os.mkdir(system_config.SYNC_INSTALLATION_FOLDER+"config/", 0o755)

    if not os.path.isfile(system_config.SYNC_INSTALLATION_FOLDER+"config/hash_file.conf"):
        try:
            with open(system_config.SYNC_INSTALLATION_FOLDER+"config/hash_file.conf", "w") as f:
                api_hash = input("Enter the app hash: ")
                f.write(str(api_hash))
                f.close()
        except IOError:
            print("Could not create or modify the file")
    else:
        if input("There is already a hash saved, do you want to rewrite it? y/N ") == "y":
            try:
                with open(system_config.SYNC_INSTALLATION_FOLDER+"config/hash_file.conf", "w") as f:
                    api_hash = input("Enter the app hash: ")
                    f.write(str(api_hash))
                    f.close()
            except IOError:
                print("Could not create or modify the file")
        else:
            print("API HASH not changed")


def save_api_config():
    os.chdir(system_config.SYNC_INSTALLATION_FOLDER+"src/")
    print("Go to https://my.telegram.org/ for activating an application and get an api id and an api hash")
    save_api_id()
    save_api_hash()
    api_id = api_config.get_api_id()
    api_hash = api_config.get_hash_id()
    client = TelegramClient("TeleSync", api_id, api_hash)
    client.start()
    client.disconnect()


if __name__ == "__main__":
    save_api_config()
