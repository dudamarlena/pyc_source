# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\IntegerType.py
# Compiled at: 2018-01-18 12:30:45
# Size of source mod 2**32: 1129 bytes
import logging, re
from ..decorators import *
from .DecimalType import DecimalType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class IntegerType(DecimalType):

    def parse_value(self, value):
        m = re.fullmatch('[\\-+]?[0-9]+', value)
        if not m:
            raise ValueError('xs:integer must match ' + p)
        return int(value)