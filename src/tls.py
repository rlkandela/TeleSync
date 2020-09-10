#!/usr/bin/env python3
"""Main module for using TeleSync as CLI or with a cron job"""
import os
from telethon import TelegramClient

import system_config
import api_config
import folder_checking
import item_checking
import item_compression
import database

import chanel_parser

def run_main(mainf):
    """Function for running the main function

    Args:
        mainf (Function): async main function that receives as parameter the client
    """
    # Changing root dir to the source dir
    os.chdir(system_config.SYNC_INSTALLATION_FOLDER+"src/")

    # Retrieving api_id and api_hash
    api_id = api_config.get_api_id()
    api_hash = api_config.get_hash_id()

    # Creating and starting the client
    client = TelegramClient('TeleSync', api_id, api_hash)
    client.start()
    client.loop.run_until_complete(mainf(client))
    client.disconnect()

async def func_main(tg_client):
    """Async main function to be run with run_main

    Args:
        tg_client (TelegramClient): telegram client already started
    """
    # CHECK IF CHANNEL EXISTS
    n_msgs = 0
    sync_valid_items = folder_checking.get_sync_valid_items(system_config.MAX_DIR_SIZE)
    d_items = await item_checking.get_files_dict(tg_client)
    uploaded_items = [*d_items]
    expanded, contracted = folder_checking.calculate_diff(uploaded_items)
    to_up_expanded = folder_checking.process_expanded(expanded, sync_valid_items)
    not_to_fwd_contracted = folder_checking.process_contracted(contracted, uploaded_items)

    for u_item in uploaded_items:
        if u_item in sync_valid_items:
            if item_checking.get_mtime(u_item) > item_checking.get_upload_time(d_items[u_item]):
                # LOCAL > UPLOADED
                # UPLOADING
                print("Uploading {}, local is newer".format(u_item))
            elif item_checking.get_mtime(u_item) < item_checking.get_upload_time(d_items[u_item]):
                # LOCAL < UPLOADED
                # DOWNLOADING
                print("Downloading {}, local is older".format(u_item))

    for item in to_up_expanded+contracted:
        if os.path.isdir(item):
            output_filename = os.path.basename(os.path.dirname(os.path.join(item,"")))
        else:
            output_filename = os.path.basename(item)
        output_filename += ".tgz"
        # compressed_item_path = item_compression.compress_item(output_filename, item)

        # TODO check if item should be uploaded


async def func_test_gdb(tg_client):
    system_config.check_all()
    await database.database_resync(tg_client)

if __name__ == "__main__":
    run_main(func_test_gdb)
