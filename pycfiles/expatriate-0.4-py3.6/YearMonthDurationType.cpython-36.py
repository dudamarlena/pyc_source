# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\YearMonthDurationType.py
# Compiled at: 2018-01-18 12:32:48
# Size of source mod 2**32: 1447 bytes
import logging, re
from ..decorators import *
from .DurationType import DurationType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class YearMonthDurationType(DurationType):

    def parse_value(self, value):
        m = re.fullmatch('-?P(\\d+Y)?(\\d+M)?', value)
        if not m or not re.fullmatch('.*[YM].*', value):
            raise ValueError('Unable to parse xs:YearMonthDuration value')
        return super().parse_value(value)

    def produce_value(self, value):
        months, seconds = value
        if seconds != 0:
            raise ValueError('xs:YearMonthDuration requires 0 for seconds value')
        return super().produce_value(value)