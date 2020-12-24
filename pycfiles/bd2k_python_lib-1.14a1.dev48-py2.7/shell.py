# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bd2k/util/shell.py
# Compiled at: 2018-05-03 13:55:55
from builtins import range
import re

def quote(s, level=1):
    for i in range(0, level):
        s = _quote(s)

    return s


_find_unsafe = re.compile('[^\\w@%+=:,./-]').search

def _quote(s):
    """
    Return a shell-escaped version of the string *s*.

    Stolen from Python 3's shlex module
    """
    if not s:
        return "''"
    else:
        if _find_unsafe(s) is None:
            return s
        return "'" + s.replace("'", '\'"\'"\'') + "'"