# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\xpath\Predicate.py
# Compiled at: 2018-01-18 12:34:05
# Size of source mod 2**32: 2049 bytes
import logging
from .exceptions import *
from .Function import Function
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Predicate(object):

    def __init__(self):
        self.children = []

    def evaluate(self, context_node, context_position, context_size, variables):
        if len(self.children) != 1:
            raise XPathSyntaxException('Predicate can only have 1 expression')
        v = self.children[0].evaluate(context_node, context_position, context_size, variables)
        if isinstance(v, bool):
            logger.debug('Boolean predicate subexpression: ' + str(v))
            return v
        else:
            if isinstance(v, int) or isinstance(v, float):
                logger.debug('Numeric result for predicate subexpression: ' + str(v) + '; comparing to position()')
                return Function.f_position((), context_node, context_position, context_size, variables) == v
            v_b = Function.f_boolean((v,), context_node, context_position, context_size, variables)
            logger.debug('Converting predicate subexpression result ' + str(v) + ' to boolean: ' + str(v_b))
            return v_b

    def __str__(self):
        return 'Predicate ' + hex(id(self)) + ': [' + ','.join([str(x) for x in self.children]) + ']'