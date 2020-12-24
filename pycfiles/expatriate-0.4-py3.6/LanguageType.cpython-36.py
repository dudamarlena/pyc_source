# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\LanguageType.py
# Compiled at: 2018-01-18 12:30:56
# Size of source mod 2**32: 1191 bytes
import logging, re
from ..decorators import *
from .TokenType import TokenType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LanguageType(TokenType):

    def parse_value(self, value):
        m = re.fullmatch('[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*', value)
        if not m:
            raise ValueError('xs:language must match [a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*')
        return super().parse_value(value)