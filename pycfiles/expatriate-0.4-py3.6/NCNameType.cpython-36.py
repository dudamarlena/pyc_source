# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\NCNameType.py
# Compiled at: 2018-01-18 12:31:13
# Size of source mod 2**32: 1166 bytes
import logging, re
from . import c_, i_
from ..decorators import *
from .NameType import NameType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class NCNameType(NameType):

    def parse_value(self, value):
        m = re.fullmatch(i_ + c_ + '*', value)
        if not m:
            raise ValueError('xs:NameType must match \\i\\c* ' + value)
        return super().parse_value(value)