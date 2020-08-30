# coding: utf-8
"""File for configuring the installation"""
import os
import sys
import shutil
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
    """Function that runs a little _installer_ INCOMPLETE"""
    if os.geteuid() != 0:
        os.chdir(system_config.SYNC_INSTALLATION_FOLDER+"src/")
        print("Go to https://my.telegram.org/ for activating an application and get an api id and an api hash")
        save_api_id()
        save_api_hash()
        api_id = api_config.get_api_id()
        api_hash = api_config.get_hash_id()
        client = TelegramClient("TeleSync", api_id, api_hash)
        client.start()
        client.disconnect()
    else:
        sys.stderr.write("Called as root, insecure, exiting.\nCall it without root permissions.\n")

def main_install():
    # Check that it's not running as root
    if os.geteuid() != 0:
        # Get the path to the source
        src_dir = os.path.dirname(sys.argv[0])
        if src_dir == "":
            src_root_dir = ".."
            src_dir = "."
        else:
            src_root_dir = os.path.dirname(src_dir)
            if src_root_dir == "":
                src_root_dir = "."
        # Change directory
        os.chdir(src_root_dir)

        # Check for the installation folder
        # TODO make it OS dependent or reimplement it for windows at least
        if not os.path.exists(system_config.SYNC_INSTALLATION_FOLDER):
            print("{} does not exist\n Creating it".format(system_config.SYNC_INSTALLATION_FOLDER))
            os.system("sudo mkdir -m 755 {}".format(system_config.SYNC_INSTALLATION_FOLDER))
            print("{} Has wrong permissions\n Changing owner to {}:{}"
                  .format(system_config.SYNC_INSTALLATION_FOLDER,os.environ["USER"],
                          os.environ["USER"]))
            os.system("sudo chown {}:{} {}".format(os.environ["USER"],os.environ["USER"],
                                                   system_config.SYNC_INSTALLATION_FOLDER))

        # Check for the subfolders
        if not os.path.exists(system_config.SYNC_INSTALLATION_FOLDER+"config/"):
            os.mkdir(system_config.SYNC_INSTALLATION_FOLDER+"config/",0o700)
        if not os.path.exists(system_config.SYNC_INSTALLATION_FOLDER+"src/"):
            os.mkdir(system_config.SYNC_INSTALLATION_FOLDER+"src/",0o700)

        if "Documents" in system_config.SYNC_INSTALLATION_FOLDER:
            print("Debug mode on, not copying files")

        for filename in os.listdir("src/"):
            # Theoretically, no checks are needed, but they are harmless and helpful
            if (not filename.endswith(".session")) and (not os.path.isdir("src/"+filename)) and (not "test" in filename) and (not "old" in filename):
                shutil.copyfile("src/"+filename,
                                system_config.SYNC_INSTALLATION_FOLDER+"src/"+filename)
    else:
        sys.stderr.write("Called as root, insecure, exiting.\nCall it without root permissions.\n")



if __name__ == "__main__":
    main_install()
    save_api_config()
