# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/plugins/generic/syntax.py
# Compiled at: 2013-12-09 06:41:17
"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
import re
from lib.core.exception import SqlmapUndefinedMethod

class Syntax:
    """
    This class defines generic syntax functionalities for plugins.
    """

    def __init__(self):
        pass

    @staticmethod
    def _escape(expression, quote=True, escaper=None):
        retVal = expression
        if quote:
            for item in re.findall("'[^']*'+", expression, re.S):
                _ = item[1:-1]
                if _:
                    retVal = retVal.replace(item, escaper(_))

        else:
            retVal = escaper(expression)
        return retVal

    @staticmethod
    def escape(expression, quote=True):
        errMsg = "'escape' method must be defined "
        errMsg += 'inside the specific DBMS plugin'
        raise SqlmapUndefinedMethod(errMsg)