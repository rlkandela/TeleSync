#!/bin/python3.8

import os
import sys
from telethon import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest#\

import api_config
import system_config
import chanel_parser
import folder_checking
import item_checking
import item_compression

def main1():
    item_compression.clear_tmp_folder()

def main2():
    for item in system_config.get_synchronized_items():
        item_compression.clear_tmp_folder()

        if os.path.isdir(item):
            ofn = os.path.basename(os.path.dirname(os.path.join(item,"")))
        else:
            ofn = os.path.basename(item)
        ofn += ".tgz"
        item_compression.compress_item(ofn,item)

        print("Se ha comprimido {}".format(ofn))
    item_compression.clear_tmp_folder()

if __name__ == "__main__":
    main2()
