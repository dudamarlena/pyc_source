# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\TimeType.py
# Compiled at: 2018-01-18 12:32:18
# Size of source mod 2**32: 1440 bytes
import datetime, logging, re
from ..decorators import *
from .AnySimpleType import AnySimpleType
from .SevenPropertyModel import SevenPropertyModel
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TimeType(AnySimpleType):

    def parse_value(self, value):
        m = re.fullmatch('(-?\\d\\d):(\\d\\d):(\\d\\d(\\.\\d+)?)((([-+])(\\d\\d):(\\d\\d))|Z)?', value)
        if not m:
            raise ValueError('Unable to parse Time value')
        m = list(m.groups())
        m.insert(0, None)
        return SevenPropertyModel(hour=(m[1]), minute=(m[2]), second=(m[3]), timezoneOffset=(m[5]))