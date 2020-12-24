# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\NMTokensType.py
# Compiled at: 2018-01-18 12:31:20
# Size of source mod 2**32: 1146 bytes
import logging, re
from ..decorators import *
from .List import List
from .NMTokenType import NMTokenType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class NMTokensType(List):

    def parse_item(self, item_value):
        return NMTokenType().parse_value(item_value)

    def produce_item(self, item_value):
        return NMTokenType().produce_value(item_value)