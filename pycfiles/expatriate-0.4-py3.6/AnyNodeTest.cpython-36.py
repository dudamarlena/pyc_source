# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\xpath\AnyNodeTest.py
# Compiled at: 2018-01-18 12:33:24
# Size of source mod 2**32: 1303 bytes
import logging
from .NodeTest import NodeTest
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AnyNodeTest(NodeTest):

    def __init__(self, principal_node_type):
        super().__init__()
        self._prinicpal_node_type = principal_node_type

    def evaluate(self, context_node, context_position, context_size, variables):
        return context_node.get_type() == self._prinicpal_node_type

    def __str__(self):
        return 'AnyNodeTest ' + hex(id(self)) + ': [' + ','.join([str(x) for x in self.children]) + ']'