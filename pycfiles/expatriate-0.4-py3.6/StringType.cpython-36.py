# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\StringType.py
# Compiled at: 2018-01-18 12:32:15
# Size of source mod 2**32: 1628 bytes
import logging, re
from ..decorators import *
from .AnySimpleType import AnySimpleType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class StringType(AnySimpleType):

    def get_value_pattern(self):
        pass

    def get_value_enum(self):
        pass

    def parse_value(self, value):
        if not isinstance(value, str):
            raise TypeError('xs:string requires a str value for initialization, got ' + value.__class__.__name__)
        else:
            p = self.get_value_pattern()
            if p is not None:
                if not re.fullmatch(p, value):
                    raise ValueError(self.__class__.__name__ + ' requires a value matching ' + p)
            e = self.get_value_enum()
            if e is not None:
                if value not in e:
                    raise ValueError(self.__class__.__name__ + ' requires a value in ' + str(e))
        return value