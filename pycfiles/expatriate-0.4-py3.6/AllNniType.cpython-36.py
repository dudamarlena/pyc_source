# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\AllNniType.py
# Compiled at: 2018-01-18 12:28:01
# Size of source mod 2**32: 1169 bytes
import logging
from ..decorators import *
from .NMTokenType import NMTokenType
from .NonNegativeIntegerType import NonNegativeIntegerType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AllNniType(NMTokenType):
    __doc__ = '\n    test\n    '

    def parse_value(self, value):
        if value == 'unbounded':
            return value
        else:
            return NonNegativeIntegerType().parse_value(value)