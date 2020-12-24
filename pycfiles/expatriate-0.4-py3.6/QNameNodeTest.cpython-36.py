# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\xpath\QNameNodeTest.py
# Compiled at: 2018-01-18 12:34:10
# Size of source mod 2**32: 1330 bytes
import logging
from .NodeTest import NodeTest
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class QNameNodeTest(NodeTest):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def evaluate(self, context_node, context_position, context_size, variables):
        if not hasattr(context_node, 'name'):
            return False
        else:
            return context_node.name == self.name

    def __str__(self):
        return 'QNameNodeTest ' + hex(id(self)) + ' ' + self.name + ': [' + ','.join([str(x) for x in self.children]) + ']'