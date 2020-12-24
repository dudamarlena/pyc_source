# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\NMTokenType.py
# Compiled at: 2018-01-18 12:31:22
# Size of source mod 2**32: 1158 bytes
import logging, re
from . import c_
from ..decorators import *
from .TokenType import TokenType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class NMTokenType(TokenType):

    def parse_value(self, value):
        m = re.fullmatch(c_ + '+', value)
        if not m:
            raise ValueError('xs:NMTOKEN must match \\c+ ' + value)
        return super().parse_value(value)