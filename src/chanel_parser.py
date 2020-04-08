# coding: utf-8
"""File for retrieving from the channel the uploaded files and its locations but not for downloading them"""
import os
import api_config
import folder_checking

async def get_messages(client):
    """Function that gets the messages sent on the channel, but just the last n specified by the last integer send. Must be awaited

    Args:
        client (TelegramClient): The already connected client

    Returns:
        list of Message: List of the objects of the messages read from the channel, if the channel does not exists, it returns an empti list and creates the channel
    """

    dialogs = await client.get_dialogs(archived=None)
    names = [i.name for i in dialogs]
    if api_config.CHANNEL_NAME in names:
        amount = await client.get_messages(api_config.CHANNEL_NAME,1)
        amount = int(amount[0].message)

        msgs = await client.get_messages(api_config.CHANNEL_NAME,amount+1)
        del msgs[0]
        return msgs
    else:
        # TODO Crear canal
        return []

def get_filenames(msgs):
    """Function that return the filenames of the items uploaded

    Args:
        msgs (list of Message): List of messages that contain an item

    Returns:
        list of str: List of strings with the filenames of the items uploaded
    """

    return [msg.media.document.attributes[0].file_name for msg in msgs]

def get_paths(msgs):
    """Function that returns the original location of the items uploaded

    Args:
        msgs (list of Message): List of messages that contain an item

    Returns:
        list of str: List of strings with the original locations of the items uploaded
    """

    return [msg.message for msg in msgs]

async def parse_uploaded_items(client):
    """Function that requests the messages and returns them along the original path. Must be awaited

    Args:
        client (TelegramClient): The already connected client

    Returns:
        (list of Message,list of str): Messages containing the uploaded items and paths to where they should go
    """

    msgs = await get_messages(client)
    filenames = get_filenames(msgs)
    uploaded_items = get_paths(msgs)
    return (msgs,uploaded_items)
