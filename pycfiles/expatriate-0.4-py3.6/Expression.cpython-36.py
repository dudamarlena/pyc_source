# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\xpath\Expression.py
# Compiled at: 2018-01-18 12:33:38
# Size of source mod 2**32: 1553 bytes
import logging, re
from .exceptions import *
from .Operator import Operator
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Expression(object):

    def __init__(self):
        self.children = []

    def evaluate(self, context_node, context_position, context_size, variables):
        logger.debug('Evaluating ' + str(self))
        if len(self.children) > 1:
            raise XPathSyntaxException('Expression has more than 1 child')
        v = self.children[0].evaluate(context_node, context_position, context_size, variables)
        logger.debug('Child ' + str(self.children[0]) + ' evaluated to ' + str(v))
        return v

    def __str__(self):
        return 'Expression ' + hex(id(self)) + ': [' + ','.join([str(x) for x in self.children]) + ']'