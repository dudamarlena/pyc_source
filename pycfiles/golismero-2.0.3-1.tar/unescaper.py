# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/lib/core/unescaper.py
# Compiled at: 2013-12-09 06:41:17
"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
from lib.core.common import Backend
from lib.core.data import conf
from lib.core.datatype import AttribDict
from lib.core.settings import EXCLUDE_UNESCAPE

class Unescaper(AttribDict):

    def escape(self, expression, quote=True, dbms=None):
        if conf.noEscape:
            return expression
        else:
            if expression is None:
                return expression
            else:
                for exclude in EXCLUDE_UNESCAPE:
                    if exclude in expression:
                        return expression

                identifiedDbms = Backend.getIdentifiedDbms()
                if dbms is not None:
                    return self[dbms](expression, quote=quote)
                if identifiedDbms is not None:
                    return self[identifiedDbms](expression, quote=quote)
                return expression

            return


unescaper = Unescaper()