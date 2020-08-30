#!/bin/python3.8

import os
import sys
import system_config
import folder_checking

def main1():
    for j,item in enumerate(system_config.get_synchronized_items()):
        print("{}: {}".format(j,item))
        if os.path.isdir(item):
            content = folder_checking.get_content(item)
            for i,itemm in enumerate(content):
                if not os.path.islink(itemm):
                    print("{}.{}: {}".format(j,i+1,itemm))

def main2():
    print("{} bytes".format(folder_checking.get_folder_size("/home/rlkandela/Documents/TeleSync_Pruebas/c")))

def main3():
    l = []
    ll = []
    for item in system_config.get_synchronized_items():
        l.append(item)
    for i in l:
        c = folder_checking.get_valid_items(i,300000)
        for v in c:
            ll.append(v)
    for elem in ll:
        print(elem)

def main4():
    c = folder_checking.get_valid_items("/home/rlkandela",300000000)
    for i in c:
        print(i)

def main5():
    for item in system_config.get_synchronized_items():
        print(item)
    print()
    for item in folder_checking.get_sync_valid_items(1):
        print(item)

if __name__ == "__main__":
    main5()
