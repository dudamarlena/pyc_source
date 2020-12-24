# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/progress.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 3225 bytes
"""module for giving information on process progress"""
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '07/08/2019'
import sys
from enum import Enum
import logging
_logger = logging.getLogger(__name__)

class _Advancement(Enum):
    step_1 = '\\'
    step_2 = '-'
    step_3 = '/'
    step_4 = '|'

    @staticmethod
    def getNextStep(step):
        if step is _Advancement.step_1:
            return _Advancement.step_2
        if step is _Advancement.step_2:
            return _Advancement.step_3
        if step is _Advancement.step_3:
            return _Advancement.step_4
        return _Advancement.step_1

    @staticmethod
    def getStep(value):
        if value % 4 == 0:
            return _Advancement.step_4
        if value % 3 == 0:
            return _Advancement.step_3
        if value % 2 == 0:
            return _Advancement.step_2
        return _Advancement.step_1


class Progress(object):
    __doc__ = 'Simple interface for defining advancement on a 100 percentage base'

    def __init__(self, name):
        self._name = name
        self.reset()

    def reset(self, max_=None):
        self._nProcessed = 0
        self._maxProcessed = max_

    def startProcess(self):
        self.setAdvancement(0)

    def setAdvancement(self, value):
        length = 20
        block = int(round(length * value / 100))
        msg = '\r{0}: [{1}] {2}%'.format(self._name, '#' * block + '-' * (length - block), round(value, 2))
        if value >= 100:
            msg += ' DONE\r\n'
        sys.stdout.write(msg)
        sys.stdout.flush()

    def endProcess(self):
        self.setAdvancement(100)

    def setMaxAdvancement(self, n):
        self._maxProcessed = n

    def increaseAdvancement(self, i=1):
        self._nProcessed += i
        self.setAdvancement(self._nProcessed / self._maxProcessed * 100)