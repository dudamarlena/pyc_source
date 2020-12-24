# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\EntitiesType.py
# Compiled at: 2018-01-18 12:29:22
# Size of source mod 2**32: 1142 bytes
import logging, re
from ..decorators import *
from .EntityType import EntityType
from .List import List
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class EntitiesType(List):

    def parse_item(self, item_value):
        return EntityType().parse_value(item_value)

    def produce_item(self, item_value):
        return EntityType().produce_value(item_value)