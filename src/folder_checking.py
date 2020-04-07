# coding: utf-8
"""File for checking if a folder can be uploaded or not given the maximum size"""
import os
import system_config


def get_content(folder):
    content = os.listdir(folder)
    ret = []
    for item in content:
        joined = os.path.join(folder,item)
        if os.path.isdir(joined):
            joined+='/'
        ret.append(joined)
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

def get_sync_valid_items(max_size):
    items = system_config.get_synchronized_items()
    ret = []
    for item in items:
        ret+=get_valid_items(item,max_size)
    return ret

def check_folder_expanded(folder, local_items):
    items = [item for item in local_items if item.startswith(folder)]
    if len(items) == 0:
        return False
    elif len(items) == 1:
        if items[0] == folder:
            return False
        else:
            return True
    else:
        return True

def check_folder_contracted(folder, uploaded_items):
    items = [item for item in uploaded_items if item.startswith(folder)]
    if len(items) == 0:
        return False
    elif len(items) == 1:
        if items[0] == folder:
            return False
        else:
            return True
    else:
        return True

def calculate_diff(uploaded_items):
    local_items = get_sync_valid_items(system_config.MAX_DIR_SIZE)
    local_folders = [item for item in local_items if os.path.isdir(item)]
    uploaded_folders = [item for item in uploaded_items if os.path.isdir(item)]

    expanded = [folder for folder in uploaded_folders if check_folder_expanded(folder, local_items)]
    contracted = [folder for folder in local_folders if check_folder_contracted(folder, uploaded_items)]
    return (expanded,contracted)

# Se subiran las devueltas, no se reenviaran las expanded
def process_expanded(expanded_folders, local_items):
    return [item for folder in expanded_folders for item in local_items if item.startswith(folder)]

# Se subiran las contracted, no se reenviaran las devueltas
def process_contracted(contracted_folders, uploaded_items):
    return [item for folder in contracted_folders for item in uploaded_items if item.startswith(folder)]
