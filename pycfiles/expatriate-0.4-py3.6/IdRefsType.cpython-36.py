# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\IdRefsType.py
# Compiled at: 2018-01-18 12:30:30
# Size of source mod 2**32: 1136 bytes
import logging, re
from ..decorators import *
from .IdRefType import IdRefType
from .List import List
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class IdRefsType(List):

    def parse_item(self, item_value):
        return IdRefType().parse_value(item_value)

    def produce_item(self, item_value):
        return IdRefType().produce_value(item_value)