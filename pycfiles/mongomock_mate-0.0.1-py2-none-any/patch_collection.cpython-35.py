# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/mongomock_mate-project/mongomock_mate/patch_collection.py
# Compiled at: 2018-07-30 23:07:59
# Size of source mod 2**32: 457 bytes
"""
monkey patch ``mongomock.collection``
"""
from mongomock.collection import Collection
from mongomock.write_concern import WriteConcern
Collection._write_concern_attr = None

@property
def _collection_write_concern(self):
    if self._write_concern_attr is None:
        self._write_concern_attr = WriteConcern()
    return self._write_concern_attr


Collection.write_concern = _collection_write_concern