# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\DbUtil.py
# Compiled at: 2005-10-16 15:50:51
__doc__ = '\nUtilities for database connections\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
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