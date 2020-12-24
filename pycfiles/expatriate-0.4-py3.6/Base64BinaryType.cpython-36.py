# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\Base64BinaryType.py
# Compiled at: 2018-01-18 12:28:44
# Size of source mod 2**32: 1314 bytes
import base64, logging, re
from ..decorators import *
from .AnySimpleType import AnySimpleType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Base64BinaryType(AnySimpleType):

    def parse_value(self, value):
        value = super().parse_value(value)
        m = re.fullmatch(b'[a-zA-Z0-9+/= ]*', value)
        if not m:
            raise ValueError('xs:Base64Binary must match [a-zA-Z0-9+/= ]*')
        return base64.b64decode(value)

    def produce_value(self, value):
        return base64.b64encode(value)