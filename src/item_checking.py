# coding: utf-8
"""File for checking if an item should be uploaded or not given the modification time"""
import os
from datetime import datetime, timezone, timedelta
import chanel_parser
import folder_checking

LOCAL_TIMEZONE = datetime.now(timezone(timedelta(0))).astimezone().tzinfo
"""Local timezone of the user calculated at the start of the app"""

async def get_files_dict(client):
    """Function that returns a dictionary with the Messages indexed by the items. Must be awaited

    Args:
        client (TelegramClient): The already started client

    Returns:
        dict(str,Message): Dictionary of messages asociated by their paths
    """

    msgs, items = await chanel_parser.parse_uploaded_items(client)
    return dict(zip(items,msgs))

def check_fwd_msg(msg):
    """Function that checks if a message is forwarded or not

    Args:
        msg (Message): Message read from the channel

    Returns:
        bool: True if the message is forwarded, False if not
    """

    if msg.fwd_from is None:
        return False
    return True

def get_upload_time(msg):
    """Function that returns the time when the item was
    uploaded conditionally if its a forwarded message or not

    Args:
        msg (Message): Message read from the channel

    Returns:
        datetime: Datetime structure with the time when the item was uploaded
    """

    if check_fwd_msg(msg):
        return msg.fwd_from.date.replace(tzinfo=timezone.utc).astimezone(tz=LOCAL_TIMEZONE)
    return msg.date.replace(tzinfo=timezone.utc).astimezone(tz=LOCAL_TIMEZONE)

def get_file_mtime(path):
    """Function that returns the modification time of an item
    If called with a folder does not calculate it recurisvely
    just considers direct modifications

    Args:
        path (str): Path to the file

    Returns:
        datetime: Datetime structure with the time of the last modification
    """
    ret=datetime.fromtimestamp(os.path.getmtime(path)).replace(microsecond=0,tzinfo=LOCAL_TIMEZONE)
    return ret

def get_dir_mtime(directory):
    """Function that returns the modification time of a folder
    calculated recursively

    Args:
        directory (str): Path to the directory

    Returns:
        datetime: Datetime structure with the time of the last modification
    """
    content = folder_checking.get_content(directory)
    # If the directory is empty, the file mtime of the folder
    # matches the last item remove or the folder creation time
    if len(content) == 0:
        return get_file_mtime(directory)

    time = datetime.fromordinal(1).replace(microsecond=0,tzinfo=LOCAL_TIMEZONE)
    for item in content:
        if not os.path.islink(item):
            if os.path.isfile(item):
                time = max(get_file_mtime(item),time)
            elif os.path.isdir(item):
                time = max(get_dir_mtime(item),time)
    return time

def get_mtime(item):
    """Function that returns the last modification time of an item.
    If this item is a folder, it is calculated recursively

    Args:
        item (str): Path to the item

    Returns:
        datetime: Datetime structure with the time of the last modification
    """
    if os.path.islink(item) or os.path.isfile(item):
        return get_file_mtime(item)
    if os.path.isdir(item):
        return get_dir_mtime(item)
    raise Exception("Error, unknown file type")
