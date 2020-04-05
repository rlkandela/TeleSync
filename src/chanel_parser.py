# coding: utf-8
"""File for checking if a folder can be uploaded or not given the maximum size"""
import os
import telethon
import api_config

async def get_messages(client):
    ret = []
    dialogs = await client.get_dialogs(archived=None)
    names = [i.name for i in dialogs]
    if api_config.CHANNEL_NAME in names:
        amount = await client.get_messages(api_config.CHANNEL_NAME,1)
        amount = int(amount[0].message)

        msgs = await client.get_messages(api_config.CHANNEL_NAME,amount+1)
        del msgs[0]
        return msgs
    else:
        return []

def get_filenames(msgs):
    return [msg.media.document.attributes[0].file_name for msg in msgs]

async def parse_uploaded_items(client):
    msgs = await get_messages(client)
    filenames = get_filenames(msgs)
