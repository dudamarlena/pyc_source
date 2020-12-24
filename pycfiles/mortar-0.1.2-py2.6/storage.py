# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mortar/storage.py
# Compiled at: 2008-12-19 12:41:15
storages = {}

def addStorage(name, storage):
    global storages
    storages[name] = storage


def getStorage(name):
    return storages[name]