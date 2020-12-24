# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\NegativeIntegerType.py
# Compiled at: 2018-01-18 12:31:15
# Size of source mod 2**32: 1160 bytes
import logging
from ..decorators import *
from .NonPositiveIntegerType import NonPositiveIntegerType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class NegativeIntegerType(NonPositiveIntegerType):

    def parse_value(self, value):
        value = super().parse_value(value)
        if value > -1:
            raise ValueError('xs:negativeInteger cannot be > -1')
        return value