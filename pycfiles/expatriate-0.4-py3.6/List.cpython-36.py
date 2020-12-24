# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\List.py
# Compiled at: 2018-01-18 12:30:59
# Size of source mod 2**32: 1800 bytes
import logging, re
from ..decorators import *
from .StringType import StringType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class List(StringType):

    def parse_value(self, value):
        value = super().parse_value(value)
        if len(value) < 1:
            raise ValueError('xs:List must contain at least 1 character')
        r = []
        for i in re.split('\\s+', value):
            r.append(self.parse_item(i))

        return tuple(r)

    def produce_value(self, value):
        r = []
        for i in value:
            r.append(self.produce_item(i))

        return ' '.join(r)

    def parse_item(self, item_value):
        import inspect
        raise NotImplementedError(inspect.stack()[0][3] + '() has not been implemented in subclass: ' + self.__class__.__name__)

    def produce_item(self, item_value):
        import inspect
        raise NotImplementedError(inspect.stack()[0][3] + '() has not been implemented in subclass: ' + self.__class__.__name__)