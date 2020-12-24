# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/featureflow/database_iterator.py
# Compiled at: 2019-03-01 22:03:23
# Size of source mod 2**32: 360 bytes
from .extractor import Node

class DatabaseIterator(Node):

    def __init__(self, needs=None, func=None):
        super(DatabaseIterator, self).__init__(needs=needs)
        self._func = func

    def _process(self, data):
        for _id in data.iter_ids():
            try:
                yield self._func(_id)
            except:
                continue