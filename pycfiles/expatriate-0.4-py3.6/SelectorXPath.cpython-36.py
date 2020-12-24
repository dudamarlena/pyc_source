# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\SelectorXPath.py
# Compiled at: 2018-01-18 12:32:00
# Size of source mod 2**32: 1495 bytes
import logging, re
from ..decorators import *
from .TokenType import TokenType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class SelectorXPath(TokenType):

    def get_value_pattern(self):
        return '(\\.//)?(((child::)?((' + i_ + c_ + '*:)?(' + i_ + c_ + '*|\\*)))|\\.)(/(((child::)?((' + i_ + c_ + '*:)?(' + i_ + c_ + '*|\\*)))|\\.))*(\\|(\\.//)?(((child::)?((' + i_ + c_ + '*:)?(' + i_ + c_ + '*|\\*)))|\\.)(/(((child::)?((' + i_ + c_ + '*:)?(' + i_ + c_ + '*|\\*)))|\\.))*)*'