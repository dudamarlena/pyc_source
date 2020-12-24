# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\LongType.py
# Compiled at: 2018-01-18 12:31:05
# Size of source mod 2**32: 1279 bytes
import logging
from ..decorators import *
from .IntegerType import IntegerType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LongType(IntegerType):

    def parse_value(self, value):
        value = super().parse_value(value)
        if value < -9223372036854775808:
            raise ValueError('xs:negativeInteger cannot be < -9223372036854775808')
        if value > 9223372036854775807:
            raise ValueError('xs:negativeInteger cannot be > 9223372036854775807')
        return value