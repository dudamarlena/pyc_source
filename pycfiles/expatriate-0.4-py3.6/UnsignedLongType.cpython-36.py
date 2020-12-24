# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\UnsignedLongType.py
# Compiled at: 2018-01-18 12:32:36
# Size of source mod 2**32: 1192 bytes
import logging
from ..decorators import *
from .NonNegativeIntegerType import NonNegativeIntegerType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class UnsignedLongType(NonNegativeIntegerType):

    def parse_value(self, value):
        value = super().parse_value(value)
        if value > 18446744073709551615:
            raise ValueError('xs:UnsignedLong cannot be > 18446744073709551615')
        return value