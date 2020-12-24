# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\xpath\Operator.py
# Compiled at: 2018-01-18 12:34:00
# Size of source mod 2**32: 8292 bytes
import logging, math
from .exceptions import *
from .Function import Function
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Operator(object):

    def op_div(left, right):
        if right == 0:
            if left > 0:
                return math.inf
            else:
                return -math.inf
        else:
            return left // right

    OPERATORS = {'*':lambda x, y: x * y, 
     '+':lambda x, y: x + y, 
     '-':lambda x, y: x - y, 
     '=':lambda x, y: x == y, 
     '!=':lambda x, y: x != y, 
     '<':lambda x, y: x < y, 
     '<=':lambda x, y: x <= y, 
     '>':lambda x, y: x > y, 
     '>=':lambda x, y: x >= y, 
     'and':lambda x, y: x and y, 
     'or':lambda x, y: x or y, 
     'mod':lambda x, y: math.fmod(x, y), 
     'div':op_div, 
     'negate':lambda x: -x}

    def __init__(self, op):
        self.op = op
        self.children = []

    def evaluate(self, context_node, context_position, context_size, variables):
        from .Axis import Axis
        if self.op == 'negate':
            left = self.children[0].evaluate(context_node, context_position, context_size, variables)
            if isinstance(left, list):
                raise XPathSyntaxException('Got negate operator with a nodeset')
            else:
                if isinstance(left, str):
                    left = Functions.f_number(left)
                else:
                    if isinstance(left, bool):
                        return not left
                    if isinstance(left, int) or isinstance(left, float):
                        pass
                    else:
                        raise XPathSyntaxException('Unknown operand: ' + str(left))
            logger.debug('Negating ' + str(left))
            return Operator.OPERATORS['negate'](left)
        left = self.children[0].evaluate(context_node, context_position, context_size, variables)
        right = self.children[1].evaluate(context_node, context_position, context_size, variables)
        if self.op in ('or', 'and'):
            left = Function.f_boolean((left,), context_node, context_position, context_size, variables)
            right = Function.f_boolean((right,), context_node, context_position, context_size, variables)
        else:
            if self.op in ('+', '-', 'div', 'mod'):
                left = Function.f_number((left,), context_node, context_position, context_size, variables)
                right = Function.f_number((right,), context_node, context_position, context_size, variables)
        if isinstance(left, list):
            if isinstance(right, list):
                for l in left:
                    l = Function.f_string((l,), context_node, context_position, context_size, variables)
                    for r in right:
                        r = Function.f_string((r,), context_node, context_position, context_size, variables)
                        logger.debug('Operator ' + str(l) + self.op + str(r))
                        if Operator.OPERATORS[self.op](l, r):
                            return True

                return False
            if isinstance(left, list):
                if isinstance(right, int) or isinstance(right, float):
                    for x in left:
                        x = Function.f_number(Function.f_string((x,), context_node, context_position, context_size, variables))
                        logger.debug('Operator ' + str(x) + self.op + str(right))
                        if Operator.OPERATORS[self.op](x, right):
                            return True

                    return False
                else:
                    if isinstance(right, str):
                        for x in left:
                            x = Function.f_string((x,), context_node, context_position, context_size, variables)
                            logger.debug('Operator ' + str(x) + self.op + str(right))
                            if Operator.OPERATORS[self.op](x, right):
                                return True

                        return False
                    if isinstance(right, bool):
                        left = Function.f_boolean((left,), context_node, context_position, context_size, variables)
                        logger.debug('Operator ' + str(left) + self.op + str(right))
                        return Operator.OPERATORS[self.op](left, right)
                raise XPathSyntaxException('Unknown right hand operand: ' + str(right))
            else:
                if isinstance(right, list):
                    if isinstance(left, int) or isinstance(left, float):
                        for x in right:
                            x = Function.f_number(Function.f_string((x,), context_node, context_position, context_size, variables))
                            logger.debug('Operator ' + str(left) + self.op + str(x))
                            if Operator.OPERATORS[self.op](left, x):
                                return True

                        return False
                    else:
                        if isinstance(left, str):
                            for x in right:
                                x = Function.f_string((x,), context_node, context_position, context_size, variables)
                                logger.debug('Operator ' + str(left) + self.op + str(x))
                                if Operator.OPERATORS[self.op](left, x):
                                    return True

                            return False
                        if isinstance(left, bool):
                            right = Function.f_boolean((right,), context_node, context_position, context_size, variables)
                            logger.debug('Operator ' + str(left) + self.op + str(right))
                            return Operator.OPERATORS[self.op](left, right)
                    raise XPathSyntaxException('Unknown left hand operand: ' + str(left))
                else:
                    if isinstance(left, bool) or isinstance(right, bool):
                        left = Function.f_boolean((left,), context_node, context_position, context_size, variables)
                        right = Function.f_boolean((right,), context_node, context_position, context_size, variables)
                        logger.debug('Operator ' + str(left) + self.op + str(right))
                        return Operator.OPERATORS[self.op](left, right)
                    if isinstance(left, int) or isinstance(left, float) or isinstance(right, int) or isinstance(right, float):
                        left = Function.f_number((left,), context_node, context_position, context_size, variables)
                        right = Function.f_number((right,), context_node, context_position, context_size, variables)
                        logger.debug('Operator ' + str(left) + self.op + str(right))
                        return Operator.OPERATORS[self.op](left, right)
        else:
            if isinstance(left, str) or isinstance(right, str):
                left = Function.f_string((left,), context_node, context_position, context_size, variables)
                right = Function.f_string((right,), context_node, context_position, context_size, variables)
                logger.debug('Operator ' + str(left) + self.op + str(right))
                return Operator.OPERATORS[self.op](left, right)
            else:
                return Operator.OPERATORS[self.op](left, right)

    def __str__(self):
        return 'Operator ' + self.op + ' ' + hex(id(self)) + ': [' + ','.join([str(x) for x in self.children]) + ']'