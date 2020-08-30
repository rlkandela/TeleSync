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

async def main1(client):
    msgs = await chanel_parser.get_messages(client)
    filenames = chanel_parser.get_filenames(msgs)
    paths = chanel_parser.get_paths(msgs)
    for f,p in zip(filenames,paths):
        if p is None:
            continue
        print("{}\t@\t{}".format(f,p))

async def main2(client):
    msgs, uploaded_items = await chanel_parser.parse_uploaded_items(client)
    expanded, contracted = folder_checking.calculate_diff(uploaded_items)
    print(expanded)     # Leer process_expanded para saber utilidad
    print(contracted)   # Leer process_contracted para saber utilidad

async def main3(client):
    d_items = await item_checking.get_files_dict(client)
    keys = [*d_items]
    up_time = item_checking.get_upload_time(d_items[keys[-1]])
    mtime = item_checking.get_mtime(keys[-1])
    print("Upl time\t{}".format(up_time))
    print("Mod time\t{}".format(mtime))
    if up_time < mtime:
        print("Hay que subirlo de nuevo")
    else:
        print("No hay que subirlo, reenviar mensaje")

async def main4(client):
    d_items = await item_checking.get_files_dict(client)
    for key in d_items:
        up_time = item_checking.get_upload_time(d_items[key])
        mtime = item_checking.get_mtime(key)
        if os.path.isdir(key):
            item_name = os.path.dirname(key)
        else:
            item_name = os.path.basename(key)

        if up_time < mtime:
            print("Hay que subir de nuevo {}".format(item_name))
        else:
            print("No hay que subir de nuevo {}, reenviar el mensaje con id {}".format(item_name,d_items[key].id))

def prepare_client(mainf):
    os.chdir(system_config.SYNC_INSTALLATION_FOLDER+"src/") 

    API_ID = api_config.get_api_id()
    API_HASH = api_config.get_hash_id()

    CLIENT = TelegramClient('TeleSync', API_ID, API_HASH)
    CLIENT.start()
    CLIENT.loop.run_until_complete(mainf(CLIENT))
    CLIENT.disconnect()

if __name__ == "__main__":
    prepare_client(main4)
