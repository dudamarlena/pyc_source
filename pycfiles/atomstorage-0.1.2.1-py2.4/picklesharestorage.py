# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.7.0-Power_Macintosh/egg/atomstorage/picklesharestorage.py
# Compiled at: 2006-08-16 13:46:51
"""
A simple pickleshare storage.

Entries are stored as dicts, using for keys the integers
as strings ("1", "2", "3", etc.) as default.
"""
from pickleshare import PickleShareDB
from atomstorage import shelvestorage

class EntryManager(shelvestorage.EntryManager):
    __module__ = __name__

    def __init__(self, location):
        self.db = PickleShareDB(location)