# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\DbUtil.py
# Compiled at: 2005-10-16 15:50:51
"""
Utilities for database connections

Copyright 2005 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
__all__ = [
 'EscapeQuotes']
try:
    from EscapeQuotesc import escape as EscapeQuotes
except ImportError:

    def EscapeQuotes(qstr):
        """
        Postgres uses single quotes for string marker, so put a
        backslash before single quotes for insertion into a database.
        Also escape backslashes.
        pre: qstr = string to be escaped
        post: return the string with all single quotes escaped
        """
        if qstr is None:
            return ''
        tmp = qstr.replace('\\', '\\\\')
        tmp = tmp.replace("'", "\\'")
        return unicode(tmp)
        return