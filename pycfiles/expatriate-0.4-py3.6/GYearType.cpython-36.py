# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\GYearType.py
# Compiled at: 2018-01-18 12:30:25
# Size of source mod 2**32: 1482 bytes
import logging, re
from ..decorators import *
from .AnySimpleType import AnySimpleType
from .SevenPropertyModel import SevenPropertyModel
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class GYearType(AnySimpleType):

    def parse_value(self, value):
        m = re.fullmatch('-?([1-9][0-9]{3,}|0[0-9]{3})(Z|(\\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?', value)
        if not m:
            raise ValueError('xs:GYear must match -?([1-9][0-9]{3,}|0[0-9]{3})(Z|(\\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?')
        m = list(m.groups())
        m.insert(0, None)
        return SevenPropertyModel(year=(m[1]), timezoneOffset=(m[2]))