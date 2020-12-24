# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\cod2.py
# Compiled at: 2016-03-08 18:42:09
__author__ = 'ThorN, ttlogic, xlr8or'
__version__ = '1.4.1'
import b3.parsers.cod, re

class Cod2Parser(b3.parsers.cod.CodParser):
    gameName = 'cod2'
    IpsOnly = False
    _logSync = 1

    def setVersionExceptions(self):
        """
        Set exceptions for this specific version of COD2
        """
        if self.gameName == 'cod2':
            if self.game.shortversion == '1.0' and not self.IpsOnly:
                self.warning('CoD2 version 1.0 has known limitations on authentication! B3 will not work properly!')
            if self.game.shortversion == '1.2':
                self.debug('Overriding pbid length for cod2 v1.2 with PB!')
                self._pbRegExp = re.compile('^[0-9a-f]{30,32}$', re.IGNORECASE)