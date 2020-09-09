# coding: utf-8
"""File for sending items to the channel as for forwarding messages"""
from typing import List
import os
import tarfile
from telethon import TelegramClient
from telethon.tl.types import Message
import system_config
import api_config


async def send_item(client: TelegramClient, item: str, quote: str) -> Message:
    """ MAY CHANGE
    Function for sending an item. Must be awaited

    Args:
        client (TelegramClient): The client already started
        item (str): Path to the item to send
        quote (str): Quote to the message, it uses the original path
    """

    with open(item,"rb") as f:
        ret = await client.send_file(api_config.CHANNEL_NAME,f,caption=quote,force_document=True)
        f.close()
    return ret

async def fwd_msgs(client: TelegramClient, msgs: List[Message]) -> Message:
    """EXPECTED TO BECOME UNUSED
    Function for forwarding a message. Must be awaited

    Args:
        client (TelegramClient): The client already started
        msgs (Message or list of Message): Message(s) to be forwarded
    """

    ret = await client.forward_messages(api_config.CHANNEL_NAME,msgs,api_config.CHANNEL_NAME)
    return ret

async def send_msg(client: TelegramClient, msg: str) -> Message:
    """Function for sending a message. Must be awaited

    Args:
        client (TelegramClient): The client already started
        msg (str): The content of the message
    """

    message = await client.send_message(api_config.CHANNEL_NAME,msg,force_document=True)
    return message
