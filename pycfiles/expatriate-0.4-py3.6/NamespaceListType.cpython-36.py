# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\NamespaceListType.py
# Compiled at: 2018-01-18 12:31:08
# Size of source mod 2**32: 1584 bytes
import logging, re
from ..decorators import *
from .List import List
from .TokenType import TokenType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class NamespaceListType(TokenType):

    def parse_item(self, item_value):
        if item_value == '##any' or item_value == '##other' or item_value == '##targetNamespace' or item_value == '##local':
            return item_value
        else:
            return Token().parse_value(item_value)

    def produce_item(self, item_value):
        if item_value == '##any' or item_value == '##other' or item_value == '##targetNamespace' or item_value == '##local':
            return item_value
        else:
            return Token().produce_value(item_value)