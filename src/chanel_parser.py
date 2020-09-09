# coding: utf-8
"""File for retrieving from the channel the uploaded files and its locations
but not for downloading them"""
from typing import List, Tuple
import os
from telethon import TelegramClient
from telethon.tl.types import Message
import api_config
import folder_checking

__all__ = ["check_for_channel",
           "get_messages",
           "get_db_message",
           "get_filenames",
           "get_paths",
           "parse_uploaded_items"]

async def check_for_channel(client: TelegramClient) -> bool:
    """Checks if the channel exists. Must be awaited

    Args:
        client (TelegramClient): The already started client

    Returns:
        bool: True if the channel exists, False if it does not
    """
    dialogs = await client.get_dialogs(archived=None)
    names = [i.name for i in dialogs]
    return api_config.CHANNEL_NAME in names

async def get_messages(client: TelegramClient) -> List[Message]:
    """PROBABLY WILL BECOME UNUSED
    Function that gets the messages sent on the channel, but just the last n specified
    by the last integer send. Must be awaited

    Args:
        client (TelegramClient): The already connected client

    Returns:
        list of Message: List of the objects of the messages read from the channel,
                         if the channel does not exists, it returns an empty
                         list and creates the channel
    """
    if await check_for_channel(client):
        amount = await client.get_messages(api_config.CHANNEL_NAME,1)
        amount = int(amount[0].message)

        msgs = await client.get_messages(api_config.CHANNEL_NAME,amount+1)
        del msgs[0]
        return msgs
    # TODO Crear canal
    return []

async def get_db_message(client: TelegramClient) -> Message:
    """Function that tries to get the database of the chanel.
    In case of not finding the channel nor the database it
    creates the channel and returns None. Must be awaited

    Args:
        client (TelegramClient): The already started client

    Returns:
        Message: The message with the last database sent, if the channel
                 does not exist, or there is no .json file, then None is returned
    """
    if await check_for_channel(client):
        async for msg in client.iter_messages(api_config.CHANNEL_NAME):
            if msg.media:
                if msg.message == "database.json":
                    return msg
    return None

def get_filenames(msgs: Message) -> List[str]:
    """Function that return the filenames of the items uploaded

    Args:
        msgs (list of Message): List of messages that contain an item

    Returns:
        list of str: List of strings with the filenames of the items uploaded
    """

    return [msg.media.document.attributes[0].file_name for msg in msgs]

def get_paths(msgs: Message) -> List[str]:
    """Function that returns the original location of the items uploaded

    Args
        msgs (list of Message): List of messages that contain an item

    Returns:
        list of str: List of strings with the original locations of the items uploaded
    """

    return [msg.message for msg in msgs]

async def parse_uploaded_items(client: TelegramClient) -> Tuple[List[Message],List[str]]:
    """Function that requests the messages and returns them along the original path. Must be awaited

    Args:
        client (TelegramClient): The already connected client

    Returns:
        (list of Message,list of str): Messages containing the
                                       uploaded items and paths to where they should go
    """

    msgs = await get_messages(client)
    # filenames = get_filenames(msgs)
    uploaded_items = get_paths(msgs)
    return (msgs,uploaded_items)
