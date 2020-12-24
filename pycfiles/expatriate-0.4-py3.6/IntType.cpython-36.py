# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\IntType.py
# Compiled at: 2018-01-18 12:30:48
# Size of source mod 2**32: 1209 bytes
import logging
from ..decorators import *
from .LongType import LongType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class IntType(LongType):

    def parse_value(self, value):
        value = super().parse_value(value)
        if value > 2147483647:
            raise ValueError('xs:int cannot be > 2147483647')
        if value < -2147483648:
            raise ValueError('xs:int cannot be < -2147483648')
        return value