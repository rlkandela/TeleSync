# coding: utf-8
"""File for compressing items to the tmp folder so they can be uploaded and some more utilites, also for uncompressing items"""
import os
import shutil
import tarfile
import system_config

def filter_func(tarinfo):
    if (not tarinfo.isfile()) and (not tarinfo.isdir()):
        return None
    return tarinfo

def check_tmp_folder():
    if not os.path.exists(system_config.TMP_FOLDER):
        os.mkdir(system_config.TMP_FOLDER,0o644)

def compress_item(output_filename, item):
    check_tmp_folder()
    with tarfile.open(system_config.TMP_FOLDER+output_filename,"w:gz") as tar:
        if os.path.isdir(item):
            arcname = os.path.basename(os.path.dirname(item))
        else:
            arcname = os.path.basename(item)
        tar.add(item,arcname=arcname,filter=filter_func)

def delete_item(item):
    if os.path.isfile(item) or os.path.islink(item):
        os.unlink(item)
    elif os.path.isdir(item):
        shutil.rmtree(item)

def clear_tmp_folder():
    check_tmp_folder()
    for item in os.listdir(system_config.TMP_FOLDER):
        item_path = os.path.join(system_config.TMP_FOLDER,item)
        delete_item(item_path)


