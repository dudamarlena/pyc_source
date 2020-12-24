# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/googlesafebrowsing/datastore.py
# Compiled at: 2010-12-12 06:18:43
"""A very simple (and slow) persistence mechanism based on the shelve module.
"""
import logging, shelve

class Error(Exception):
    pass


class DataStore(object):
    """
  Changes made to mutable objects returned from a DataStore are automatically
  written back to the persistent store. Python strs are not mutable, so SetWrKey
  and SetClientKey must be used. For the List objects, use GetLists to get a
  mutable dict. Any changes to this dict and the List objects it contains will
  be written back to persistent storage when Sync is called.
  """
    LISTS = 'lists'
    WRKEY = 'wrkey'
    CLIENTKEY = 'clientkey'

    def __init__(self, basefile, create=True):
        flags = 'w'
        if create:
            flags = 'c'
        try:
            self._db = shelve.open(basefile, flag=flags, writeback=True)
        except Exception, e:
            raise Error(e)

        self._db.setdefault(DataStore.LISTS, {})
        self._db.setdefault(DataStore.WRKEY, None)
        self._db.setdefault(DataStore.CLIENTKEY, None)
        return

    def Sync(self):
        """
    This is very slow. Also, it will replace the objects in the database with
    new copies so that existing references to the old objects will no longer
    update the datastore. E.g., you must call GetLists() again after calling
    this.
    """
        self._db.sync()

    def GetLists(self):
        """
    Return a dict of listname:sblist.List. Changes to this dict and the List
    objects in it are written back to the data store when Sync is called.
    """
        return self._db[DataStore.LISTS]

    def GetWrKey(self):
        return self._db[DataStore.WRKEY]

    def SetWrKey(self, wrkey):
        self._db[DataStore.WRKEY] = wrkey

    def GetClientKey(self):
        """
    Unescaped client key.
    """
        return self._db[DataStore.CLIENTKEY]

    def SetClientKey(self, clientkey):
        self._db[DataStore.CLIENTKEY] = clientkey