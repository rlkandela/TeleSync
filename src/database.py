#!/usr/bin/env python3

from typing import Dict, Union, List
import os
import shutil
import json
from telethon import TelegramClient
from telethon.tl.types import Message
import chanel_parser
import system_config
import folder_checking
import item_sending
import item_checking
import item_compression

DBEntry = Dict[str,Union[List[int],str]]
DB = Dict[str,Dict[str,DBEntry]]

def basic_db_shape() -> DBEntry:
    """Function for getting the basic shape of a db entry
    "msg_id":[],
    "path":"",
    "upl_timestamp":[]

    Args
    Returns:
        DBEntry: Basic empty shape
    """
    return {"msg_id":[],
            "path":"",
            "upl_timestamp":[]}

async def database_download(client: TelegramClient) -> str:
    """Function that downloads the database from telegram. Must be awaited

    Args:
        client (TelegramClient): The client already started

    Returns:
        str: Path to the downloaded database, empty string in case it fails
    """
    msg = await chanel_parser.get_db_message(client)
    if not msg:
        return ""
    path = system_config.TMP_FOLDER+msg.media.document.attributes[0].file_name
    await client.download_media(msg,path)
    return path

async def database_sync(client: TelegramClient):
    """Function that downloads and updates the cached database if exists. Must be awaited

    Args:
        client (TelegramClient): The client already started
    """
    path = await database_download(client)
    if path != "":
        shutil.move(path, system_config.CACHE_FOLDER+"database.json")
    else:
        empty_db: DB = {"database":{}}
        with open(system_config.CACHE_FOLDER+"database.json","w") as open_file:
            json.dump(empty_db, open_file)

def database_load() -> DB:
    """Function that loads from the a local file the database

    Returns:
        DB: Database cargada
    """
    with open(system_config.CACHE_FOLDER+"database.json","r") as opened_file:
        ret = json.load(opened_file)
    return ret

def database_dump(database: DB):
    """Function that dumps the database to file

    Returns:
        DB: Database cargada
    """
    with open(system_config.CACHE_FOLDER+"database.json","w") as opened_file:
        json.dump(database,opened_file)

async def database_update(tg_client: TelegramClient, database: DB, elems: List[str]) -> DB:
    """Function for performing a update with the local elements in the database

    Args:
        tg_client (TelegramClient): The client already started
        database (DB): Database already loaded
        elems (List[str]): List of local elements to sync
    """
    for key in database["database"].keys():
        if not key in elems:
            # TODO download, new file
            print(key+" bajar nuevo item")

    for item in elems:
        if os.path.isdir(item):
            continue
        if not item in database["database"]:
            print(item+" added")
            ofn = os.path.basename(item) + ".tgz"
            c_item = item_compression.compress_item(ofn, item)
            msg = await item_sending.send_item(tg_client,c_item,item)
            database["database"][item]=basic_db_shape()
            database["database"][item]["msg_id"].insert(0, msg.id)
            database["database"][item]["path"] = item
            database["database"][item]["upl_timestamp"].insert(0, item_checking.get_mtime(item).timestamp())

        if database["database"][item]["upl_timestamp"][0] < item_checking.get_mtime(item).timestamp():
            print(item+" downloaded")
            ofn = os.path.basename(item) + ".tgz"
            c_item = item_compression.compress_item(ofn, item)
            msg = await item_sending.send_item(tg_client,c_item,item)
            database["database"][item]["msg_id"].insert(0, msg.id)
            database["database"][item]["upl_timestamp"].insert(0, item_checking.get_mtime(item).timestamp())
        elif database["database"][item]["upl_timestamp"][0] > item_checking.get_mtime(item).timestamp():
            # TODO Make download for multi-pc
            print(item + " bajar")

        item_compression.clear_tmp_folder()
    return database

async def database_upload(tg_client: TelegramClient) -> Message:
    """Function for uploading the local database to Telegram

    Args:
        tg_client (TelegramClient): The client already started
    """
    ret = await item_sending.send_item(tg_client,
                                       system_config.CACHE_FOLDER+"database.json",
                                       "database.json")
    return ret

async def database_resync(client: TelegramClient):
    """Function that downloads and updates the cached database if exists
    or creates a void one if it doesn't. Must be awaited

    Args:
        client (TelegramClient): The client already started
    """
    await database_sync(client)
    elems = folder_checking.get_sync_valid_items(0)
    sys_db = database_load()
    sys_db_updated = await database_update(client, sys_db, elems)
    database_dump(sys_db_updated)
    await database_upload(client)
