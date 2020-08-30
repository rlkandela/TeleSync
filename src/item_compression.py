# coding: utf-8
"""File for compressing items to the tmp folder so they can be uploaded and some more utilites, also for uncompressing items"""
import os
import shutil
import tarfile
import system_config

def filter_func(tarinfo):
    """Filter function for filtering all items that aren't files or directories

    Args:
        tarinfo (TarInfo): TarInfo of the item to be filtered

    Returns:
        TarInfo: The same `tarinfo` if it's a folder or a file or None if it is not
    """

    if (not tarinfo.isfile()) and (not tarinfo.isdir()):
        return None
    return tarinfo

def check_tmp_folder():
    """Function that checks if the temporary folder exists and in case it doesn't it creates it"""

    if not os.path.exists(system_config.TMP_FOLDER):
        os.mkdir(system_config.TMP_FOLDER,0o755)

def compress_item(output_filename, item):
    """Function for compressing an item

    Args:
        output_filename (str): Name of the compressed item
        item (str): Path to the uncompressed item

    Returns:
        str: Path to the compressed item
    """

    check_tmp_folder()
    output_item = system_config.TMP_FOLDER+output_filename
    with tarfile.open(output_item,"w:gz") as tar:
        if os.path.isdir(item):
            arcname = os.path.basename(os.path.dirname(item))
        else:
            arcname = os.path.basename(item)
        tar.add(item,arcname=arcname,filter=filter_func)
    return output_item

def delete_item(item):
    """Function that deletes an item if it is a file, link or folder

    Args:
        item (str): Path to the item to remove
    """

    if os.path.isfile(item) or os.path.islink(item):
        os.unlink(item)
    elif os.path.isdir(item):
        shutil.rmtree(item)

def clear_tmp_folder():
    """Function for clearing the temporary folder"""

    check_tmp_folder()
    for item in os.listdir(system_config.TMP_FOLDER):
        item_path = os.path.join(system_config.TMP_FOLDER,item)
        delete_item(item_path)


