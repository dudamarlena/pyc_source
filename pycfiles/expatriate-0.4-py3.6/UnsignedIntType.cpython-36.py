# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\UnsignedIntType.py
# Compiled at: 2018-01-18 12:32:33
# Size of source mod 2**32: 1152 bytes
import logging
from ..decorators import *
from .UnsignedLongType import UnsignedLongType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class UnsignedIntType(UnsignedLongType):

    def parse_value(self, value):
        value = super().parse_value(value)
        if value > 4294967295:
            raise ValueError('xs:UnsignedInt cannot be > 4294967295')
        return value