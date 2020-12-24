# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\ByteType.py
# Compiled at: 2018-01-18 12:28:46
# Size of source mod 2**32: 1187 bytes
import logging
from ..decorators import *
from .ShortType import ShortType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ByteType(ShortType):

    def parse_value(self, value):
        value = super().parse_value(value)
        if value < -128:
            raise ValueError('xs:byte cannot be < -128')
        if value > 127:
            raise ValueError('xs:byte cannot be > 127')
        return value