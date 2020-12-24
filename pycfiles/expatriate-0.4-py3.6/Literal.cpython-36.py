# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\xpath\Literal.py
# Compiled at: 2018-01-18 12:33:47
# Size of source mod 2**32: 1173 bytes
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Literal(object):

    def __init__(self, value):
        self.value = value

    def evaluate(self, context_node, context_position, context_size, variables):
        return self.value

    def __str__(self):
        return 'Literal ' + hex(id(self)) + ': ' + str(self.value)

    def __repr__(self):
        return repr(self.value)