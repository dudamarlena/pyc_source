# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wmdlib\samples\app.py
# Compiled at: 2007-09-10 19:02:59
from wmdlib.lowlevel.mswmdm import *
from wmdlib.lowlevel.devicedict import devices

def print_storage(storage, depth):
    print '\t' * depth, storage.GetName()
    storages = storage.GetStorages()
    for key in storages:
        print_storage(storages[key], depth + 1)


def main():
    for key in devices:
        print key
        storages = devices[key].GetStorages()
        depth = 1
        for key in storages:
            print_storage(storages[key], depth)


if __name__ == '__main__':
    main()