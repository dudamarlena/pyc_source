# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/storage/premade.py
# Compiled at: 2016-03-04 03:26:39
"""
Most common classes of storages
"""
from .multi import MultiStorage
from .batch import ZEOBatchStorage

class DefaultServerStorage(ZEOBatchStorage, MultiStorage):
    pass