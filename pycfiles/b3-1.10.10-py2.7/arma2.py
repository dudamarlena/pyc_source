# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\arma2.py
# Compiled at: 2016-03-08 18:42:09
from b3.parsers.battleye.abstractParser import AbstractParser
__author__ = '82ndab-Bravo17'
__version__ = '0.3'

class Arma2Parser(AbstractParser):
    gameName = 'arma2'

    def startup(self):
        """
        Called after the parser is created before run().
        """
        AbstractParser.startup(self)