# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\xpath\RootStep.py
# Compiled at: 2018-01-18 12:34:13
# Size of source mod 2**32: 1451 bytes
import logging
from .Step import Step
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class RootStep(Step):

    def __init__(self, document):
        self.children = []
        self._document = document

    def evaluate(self, context_node, context_position, context_size, variables):
        if len(self.children) == 0:
            logger.debug('Root step with no children: using ' + str(self._document) + ' as the result set')
            return [
             self._document]
        else:
            return super().evaluate(self._document, 1, 1, variables)

    def __str__(self):
        return 'RootStep ' + hex(id(self)) + ': [' + ','.join([str(x) for x in self.children]) + ']'