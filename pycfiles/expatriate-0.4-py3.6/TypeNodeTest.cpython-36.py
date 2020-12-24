# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\xpath\TypeNodeTest.py
# Compiled at: 2018-01-18 12:34:21
# Size of source mod 2**32: 1534 bytes
import logging
from .NodeTest import NodeTest
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TypeNodeTest(NodeTest):
    NODE_TYPES = [
     'comment',
     'text',
     'processing-instruction',
     'node']

    def __init__(self, name):
        super().__init__()
        self.name = name

    def evaluate(self, context_node, context_position, context_size, variables):
        if self.name == 'node':
            return True
        else:
            return context_node.get_type() == self.name

    def __str__(self):
        return 'TypeNodeTest ' + hex(id(self)) + ' ' + self.name + ': [' + ','.join([str(x) for x in self.children]) + ']'