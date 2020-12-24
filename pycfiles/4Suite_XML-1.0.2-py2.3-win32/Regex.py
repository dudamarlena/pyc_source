# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\Regex.py
# Compiled at: 2005-01-26 23:47:36
"""
Tools to manage the many different flavors of regex

Copyright 2004 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
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