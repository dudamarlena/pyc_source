# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/dbmeta.py
# Compiled at: 2014-07-11 17:28:21
__doc__ = '\nStores metadata to the "metadata" table in backend.\nUsed for import metadata, as a key-value store.\nEx: bta-import database format version\n'

class DBMetadataEntry(object):

    def __init__(self, backend):
        self.backend = backend
        self.log = backend.open_table('metadata')
        self.log.ensure_created()

    def get_value(self, key):
        """Get metadata value.

        :returns: None if value does not exist

        """
        result = self.log.find_one({key: {'$exists': 'true'}})
        if result is None:
            return
        else:
            return result[key]

    def set_value(self, key, value):
        """Set or update metadata value"""
        self.log.update({key: {'$exists': 'true'}}, {key: value}, True, multi=False)