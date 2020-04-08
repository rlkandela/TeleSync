# coding: utf-8
"""File for sending items to the channel as for forwarding messages"""
import os
import tarfile
import system_config
import api_config

async def send_item(client, item, original_path):
    """Function for sending an item. Must be awaited

    Args:
        client (TelegramClient): The client already started
        item (str): Path to the item to send
        original_path (str): Quote to the message, it uses the original path
    """

    with open(item,"rb") as f:
        await client.send_file(api_config.CHANNEL_NAME,f,caption=original_path,force_document=True)
        f.close()

async def fwd_msgs(client,msgs):
    """Function for forwarding a message. Must be awaited

    Args:
        client (TelegramClient): The client already started
        msgs (Message or list of Message): Message(s) to be forwarded
    """

    await client.forward_messages(api_config.CHANNEL_NAME,msgs,api_config.CHANNEL_NAME)

async def send_msg(client,msg):
    """Function for sending a message. Must be awaited

    Args:
        client (TelegramClient): The client already started
        msg (str): The content of the message
    """

    await client.send_message(api_config.CHANNEL_NAME,msg,force_document=True)
