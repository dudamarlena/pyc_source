# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\Regex.py
# Compiled at: 2005-01-26 23:47:36
__doc__ = '\nTools to manage the many different flavors of regex\n\nCopyright 2004 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import re
MIN_LENGTH_SEQ_PAT = re.compile('(\\(.+\\))\\{([0-9]+),\\}')

def W3cRegexToPyRegex(w3cregex):
    """
    Convert W3C regex to Python regex
    e.g.:
    >>> from Ft.Lib.Regex import W3cRegexToPyRegex
    >>> print repr(W3cRegexToPyRegex(u"(foo){5,}"))
    u'((foo)){5}(foo)*'
    """
    regex = MIN_LENGTH_SEQ_PAT.subn(lambda m: '(' + m.group(1) + ')' + '{' + m.group(2) + '}' + m.group(1) + '*', w3cregex)[0]
    return regex