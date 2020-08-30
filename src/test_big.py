#!/bin/python3.8

import os
import sys
from telethon import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest#\

import system_config
import api_config
import folder_checking
import item_checking
import item_compression
import item_sending

def prepare_client(mainf):
    # TODO cambiar por algún lugar mas significativo, como .config
    os.chdir(system_config.SYNC_INSTALLATION_FOLDER+"src/") 

    API_ID = api_config.get_api_id()
    API_HASH = api_config.get_hash_id()

    CLIENT = TelegramClient('TeleSync', API_ID, API_HASH)
    CLIENT.start()
    CLIENT.loop.run_until_complete(mainf(CLIENT))
    CLIENT.disconnect()

async def main_big(client):
    n_msgs = 0
    sync_valid_items = folder_checking.get_sync_valid_items(system_config.MAX_DIR_SIZE)
    d_items = await item_checking.get_files_dict(client)
    expanded,contracted = folder_checking.calculate_diff([*d_items])
    to_up_e = folder_checking.process_expanded(expanded,sync_valid_items)
    not_to_fwd_c = folder_checking.process_contracted(contracted, [*d_items])
    # print("A subir item de expandidas")
    # print(to_up_e)
    # print("Y a subir contraidas")
    # print(contracted)
    # print("A no reenviar expandidas")
    # print(expanded)
    # print("Y a no reenviar item de contraidas")
    # print(not_to_fwd_c)
    for item in to_up_e+contracted:
        if os.path.isdir(item):
            ofn = os.path.basename(os.path.dirname(os.path.join(item,"")))
        else:
            ofn = os.path.basename(item)
        ofn+=".tgz"
        c_item_path = item_compression.compress_item(ofn,item)
        # print("Compressed item to {}".format(ofn))
        await item_sending.send_item(client,c_item_path,item)
        n_msgs += 1
        item_compression.clear_tmp_folder()
    for item in expanded+not_to_fwd_c:
        del d_items[item]
    for item in [*d_items]+to_up_e+contracted:
        sync_valid_items.remove(item)
    for item in sync_valid_items:
        if os.path.isdir(item):
            ofn = os.path.basename(os.path.dirname(os.path.join(item,"")))
        else:
            ofn = os.path.basename(item)
        ofn += ".tgz"
        c_item_path = item_compression.compress_item(ofn,item)
        await item_sending.send_item(client,c_item_path,item)
        n_msgs += 1
        item_compression.clear_tmp_folder()
    await item_sending.fwd_msgs(client,list(d_items.values()))
    n_msgs += len([*d_items])
    await item_sending.send_msg(client,str(n_msgs))
    

if __name__ == "__main__":
    prepare_client(main_big)
    

