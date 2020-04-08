# coding: utf-8
"""File for checking if an item should be uploaded or not given the modification time"""
import os
import chanel_parser
from datetime import datetime, timezone, timedelta

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
    else:
        return True

def get_upload_time(msg):
    """Function that returns the time when the item was uploaded conditionally if its a forwarded message or not

    Args:
        msg (Message): Message read from the channel

    Returns:
        datetime: Datetime structure with the time when the item was uploaded
    """

    if check_fwd_msg(msg):
        return msg.fwd_from.date.replace(tzinfo=timezone.utc).astimezone(tz=LOCAL_TIMEZONE)
    else:
        return msg.date.replace(tzinfo=timezone.utc).astimezone(tz=LOCAL_TIMEZONE)

def get_mtime(item):
    """Function that returns the modification time of an item

    Args:
        item (str): Path to the item

    Returns:
        datetime: Datetime structure with the time of the last modification
    """

    return datetime.fromtimestamp(os.path.getmtime(item)).replace(microsecond=0,tzinfo=LOCAL_TIMEZONE)


