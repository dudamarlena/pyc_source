# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/store/versioned_item.py
# Compiled at: 2018-11-17 20:47:49
# Size of source mod 2**32: 884 bytes
from collections import namedtuple

class VersionedItem(namedtuple('VersionedItem', ['symbol', 'library', 'data', 'version', 'metadata', 'host'])):
    __doc__ = '\n    Class representing a Versioned object in VersionStore.\n    '

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