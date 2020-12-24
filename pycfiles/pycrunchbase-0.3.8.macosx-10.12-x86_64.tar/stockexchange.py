# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/pycrunchbase/resource/stockexchange.py
# Compiled at: 2017-01-13 23:45:16
import six
from .node import Node

@six.python_2_unicode_compatible
class StockExchange(Node):
    """Represents a Website on CrunchBase"""
    KNOWN_PROPERTIES = [
     'name',
     'short_name',
     'symbol',
     'created_at',
     'updated_at']

    def __str__(self):
        return ('{name} {symbol}').format(name=self.name, symbol=self.symbol)

    def __repr__(self):
        return self.__str__()