# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\HexBinaryType.py
# Compiled at: 2018-01-18 12:30:27
# Size of source mod 2**32: 1312 bytes
import binascii, logging, re
from ..decorators import *
from .AnySimpleType import AnySimpleType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class HexBinaryType(AnySimpleType):

    def parse_value(self, value):
        value = super().parse_value(value)
        m = re.fullmatch(b'([0-9a-fA-F]{2})*', value)
        if not m:
            raise ValueError('xs:HexBinary must match ([0-9a-fA-F]{2})*')
        return binascii.a2b_hex(value)

    def produce_value(self, value):
        return binascii.b2a_hex(value)