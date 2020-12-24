# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmi/parser/null.py
# Compiled at: 2018-12-29 12:21:47
from pysmi.parser.base import AbstractParser

class NullParser(AbstractParser):
    __module__ = __name__

    def __init__(self, startSym='mibFile', tempdir=''):
        pass

    def reset(self):
        pass

    def parse(self, data, **kwargs):
        return []