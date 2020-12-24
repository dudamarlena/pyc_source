# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/featureflow/iteratornode.py
# Compiled at: 2019-03-01 22:03:23
# Size of source mod 2**32: 222 bytes
from .extractor import Node

class IteratorNode(Node):

    def __init__(self, needs=None):
        super(IteratorNode, self).__init__(needs=needs)

    def _process(self, data):
        for x in data:
            yield x