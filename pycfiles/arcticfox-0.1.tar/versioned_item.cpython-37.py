# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/store/versioned_item.py
# Compiled at: 2018-11-17 20:47:49
# Size of source mod 2**32: 884 bytes
from collections import namedtuple

class VersionedItem(namedtuple('VersionedItem', ['symbol', 'library', 'data', 'version', 'metadata', 'host'])):
    """VersionedItem"""

    def __new__(cls, symbol, library, data, version, metadata, host=None):
        return super(VersionedItem, cls).__new__(cls, symbol, library, data, version, metadata, host)

    def metadata_dict(self):
        return {'symbol':self.symbol, 
         'library':self.library,  'version':self.version}

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'VersionedItem(symbol=%s,library=%s,data=%s,version=%s,metadata=%s,host=%s)' % (
         self.symbol, self.library, type(self.data), self.version, self.metadata, self.host)


ChangedItem = namedtuple('ChangedItem', ['symbol', 'orig_version', 'new_version', 'changes'])