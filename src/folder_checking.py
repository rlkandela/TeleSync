# coding: utf-8
"""File for checking if a folder can be uploaded or not given the maximum size"""
import os
import system_config

SYNC_ITEMS = system_config.get_synchronized_items()

def get_content(folder):
    content = os.listdir(folder)
    ret = []
    for item in content:
        ret.append(os.path.join(folder,item))
    return ret

def get_folder_size(folder):
    ret = 0
    for item in get_content(folder):
        if os.path.isfile(item):
            ret += os.path.getsize(item)
        elif os.path.isdir(item):
            ret+=get_folder_size(item)
    return ret

def get_valid_items(or_item, max_size):
    ret = []
    if(os.path.isfile(or_item)):
        ret.append(or_item)
    elif(get_folder_size(or_item) > max_size):
        content = get_content(or_item)
        for item in content:
            if os.path.isfile(item):
                ret.append(item)
            elif os.path.isdir(item):
                c = get_valid_items(item,max_size)
                for i in c:
                    ret.append(i)
    else:
        ret.append(or_item)

    return ret

