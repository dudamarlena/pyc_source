# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bdgt/importer/types.py
# Compiled at: 2014-10-09 13:38:05
from collections import namedtuple
ParsedTx = namedtuple('ParsedTx', ['date', 'amount', 'account', 'description'])

class ImportTx(object):

    def __init__(self, parsed_tx):
        self._parsed_tx = parsed_tx
        self._processed = False
        self._category = ''

    @property
    def parsed_tx(self):
        return self._parsed_tx

    @property
    def processed(self):
        return self._processed

    @processed.setter
    def processed(self, value):
        self._processed = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value