# coding: utf-8
"""File for checking if an item should be uploaded or not given the modification time"""
import os
import chanel_parser
from datetime import datetime, timezone, timedelta

LOCAL_TIMEZONE = datetime.now(timezone(timedelta(0))).astimezone().tzinfo

async def get_files_dict(client):
    msgs, items = await chanel_parser.parse_uploaded_items(client)
    return dict(zip(items,msgs))

def check_fwd_msg(msg):
    if msg.fwd_from is None:
        return False
    else:
        return True

def get_upload_time(msg):
    if check_fwd_msg(msg):
        return msg.fwd_from.date.replace(tzinfo=timezone.utc).astimezone(tz=LOCAL_TIMEZONE)
    else:
        return msg.date.replace(tzinfo=timezone.utc).astimezone(tz=LOCAL_TIMEZONE)

def get_mtime(item):
    return datetime.fromtimestamp(os.path.getmtime(item)).replace(microsecond=0,tzinfo=LOCAL_TIMEZONE)


