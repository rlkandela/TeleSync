# coding: utf-8
"""File for checking if a folder can be uploaded or not given the maximum size, also provides some utilites like expnsion and compression of folder checking"""
import os
import system_config


def get_content(folder):
    """Function for getting the elements inside a folder

    Args:
        folder (str): Path to the folder

    Returns:
        list of str: List of paths to the items inside the folder
    """

    content = os.listdir(folder)
    ret = []
    for item in content:
        joined = os.path.join(folder,item)
        if os.path.isdir(joined):
            joined+='/'
        ret.append(joined)
    return ret

def get_folder_size(folder):
    """Function for calculating the size of a folder summing up the elements inside it

    Args:
        folder (str): Path to the folder

    Returns:
        int: Amount of bytes of the folder
    """

    ret = 0
    for item in get_content(folder):
        if os.path.isfile(item):
            ret += os.path.getsize(item)
        elif os.path.isdir(item):
            ret+=get_folder_size(item)
    return ret

def get_valid_items(or_item, max_size):
    """Function for expanding a configured for synchronization item into some smaller items to be easier to upload them

    Args:
        or_item (str): Path to the item from the config file
        max_size (int): Amount of bytes that a folder can weight as maximum

    Returns:
        list of str: List of paths to the subitems the original one was divided into
    """

    ret = []
    if os.path.isfile(or_item):
        ret.append(or_item)
    elif os.path.isdir(or_item):
        if(get_folder_size(or_item) > max_size):
            content = get_content(or_item)
            for item in content:
                if os.path.isfile(item):
                    ret.append(item)
                elif os.path.isdir(item):
                    ret+=get_valid_items(item,max_size)
        else:
            ret.append(os.path.join(or_item,""))
    return ret

def get_sync_valid_items(max_size):
    """Function that separates all the items configured for synchronization bigger than allowed into other smaller

    Args:
        max_size (int): Maximum amount in bytes that a folder can take

    Returns:
        list of str: List of paths to all the items that are files or dirs smaller than `max_size`
    """

    items = system_config.get_synchronized_items()
    ret = []
    for item in items:
        ret+=get_valid_items(item,max_size)
    return ret

def check_folder_expanded(folder, local_items):
    """Function that checks if a folder has been expanded or not

    Args:
        folder (str): Path to the folder to check
        local_items (list of str): List of items that might get uploaded

    Returns:
        bool: True if the folder was expanded, False if not
    """

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
    """Function that checks if a folder has been compressed or not

    Args:
        folder (str): Path to the folder to check
        local_items (list of str): List of items read from the channel

    Returns:
        bool: True if the folder was compressed, False if not
    """

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
    """Function that calculates all the folders compressed and expanded

    Args:
        uploaded_items (list of str): List of paths read from the channel

    Returns:
        (list of str,list of str): List of expanded items and list of contracted items respectively
    """

    local_items = get_sync_valid_items(system_config.MAX_DIR_SIZE)
    local_folders = [item for item in local_items if os.path.isdir(item)]
    uploaded_folders = [item for item in uploaded_items if os.path.isdir(item)]

    expanded = [folder for folder in uploaded_folders if check_folder_expanded(folder, local_items)]
    contracted = [folder for folder in local_folders if check_folder_contracted(folder, uploaded_items)]
    return (expanded,contracted)

# Se subiran las devueltas, no se reenviaran las expanded
def process_expanded(expanded_folders, local_items):
    """Function that returns the afected items by the expanded folders, the returned items will get uploaded, the `expanded_folders` won't get forwarded

    Args:
        expanded_folders (list of str): List of all the folders that get expanded
        local_items (list of str): List of all the local items that might get uploaded

    Returns:
        list of str: Items that will get uploaded as consequence of the folders in `expanded_folders` got expanded
    """

    return [item for folder in expanded_folders for item in local_items if item.startswith(folder)]

# Se subiran las contracted, no se reenviaran las devueltas
def process_contracted(contracted_folders, uploaded_items):
    """Function that returns the afected items by the contracted folders, the returned items won't get forwarded, the `contracted_folders` will get uploaded

    Args:
        contracted_folders (list of str): List of folders that got contracted
        uploaded_items (list of str): List of items that were read from the channel

    Returns:
        list of str: Items that won't get forwarded as consequence of the folders in `contracted_folders` got contracted
    """

    return [item for folder in contracted_folders for item in uploaded_items if item.startswith(folder)]
