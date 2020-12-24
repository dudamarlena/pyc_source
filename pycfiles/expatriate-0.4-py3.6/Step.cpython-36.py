# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\xpath\Step.py
# Compiled at: 2018-01-18 12:34:18
# Size of source mod 2**32: 2618 bytes
import logging
from .Axis import Axis
from .exceptions import *
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Step(object):

    def __init__(self):
        self.children = []

    def evaluate(self, context_node, context_position, context_size, variables):
        from ..Document import Document
        if len(self.children) == 1:
            logger.debug('Collecting nodes with ' + str(self.children[0]) + ' for context node ' + str(context_node))
            ns = self.children[0].evaluate(context_node, context_position, context_size, variables)
            logger.debug('Nodes from ' + str(self.children[0]) + ': [' + ','.join([str(x) for x in ns]) + ']')
            logger.debug(str(self) + ' nodeset: [' + ','.join([str(x) for x in ns]) + ']')
            return ns
        if len(self.children) == 2:
            logger.debug('Collecting context nodes with ' + str(self.children[0]) + ' for context node ' + str(context_node))
            context_nodes = self.children[0].evaluate(context_node, context_position, context_size, variables)
            logger.debug('Context nodes from ' + str(self.children[0]) + ': [' + ','.join([str(x) for x in context_nodes]) + ']')
            ns = []
            for i, cn in enumerate(context_nodes):
                logger.debug('Evaluating ' + str(self.children[1]) + ' with context ' + str(cn))
                ns.extend(self.children[1].evaluate(cn, i + 1, len(context_nodes), variables))

            ns = Document.order_sort(ns)
            logger.debug(str(self) + ' nodeset: [' + ','.join([str(x) for x in ns]) + ']')
            return ns
        raise XPathSyntaxException('Steps require between 1 and 2 children')

    def __str__(self):
        return 'Step ' + hex(id(self)) + ': [' + ','.join([str(x) for x in self.children]) + ']'