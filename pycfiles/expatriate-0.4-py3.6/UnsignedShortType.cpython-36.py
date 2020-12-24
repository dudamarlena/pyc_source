# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\UnsignedShortType.py
# Compiled at: 2018-01-18 12:32:39
# Size of source mod 2**32: 1143 bytes
import logging
from ..decorators import *
from .UnsignedIntType import UnsignedIntType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class UnsignedShortType(UnsignedIntType):

    def parse_value(self, value):
        value = super().parse_value(value)
        if value > 65535:
            raise ValueError('xs:UnsignedShort cannot be > 65535')
        return value