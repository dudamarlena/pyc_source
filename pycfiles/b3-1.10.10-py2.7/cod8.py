# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\cod8.py
# Compiled at: 2016-03-08 18:42:09
__author__ = 'NTAuthority'
__version__ = '0.4'
import b3.parsers.cod6, re

class Cod8Parser(b3.parsers.cod6.Cod6Parser):
    gameName = 'cod8'
    _guidLength = 16
    _regPlayer = re.compile('(?P<slot>[0-9]+)\\s+(?P<score>[0-9-]+)\\s+(?P<ping>[0-9]+)\\s+(?P<guid>[a-z0-9]+)\\s+(?P<name>.*?)\\s+(?P<last>[0-9]+)\\s+(?P<ip>[0-9.]+):(?P<port>[0-9-]+)', re.IGNORECASE)

    def startup(self):
        """
        Called after the parser is created before run().
        """
        b3.parsers.cod6.Cod6Parser.startup(self)