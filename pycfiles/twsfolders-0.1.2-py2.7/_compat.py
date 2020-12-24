# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twsfolders/_compat.py
# Compiled at: 2014-07-04 02:20:56
import sys
PY3 = sys.version_info[0] == 3
if PY3:
    string_types = (
     str,)
    integer_types = (int,)
    text_type = str
else:
    string_types = (
     basestring,)
    integer_types = (int, long)
    text_type = unicode

def is_string(value):
    if isinstance(value, string_types):
        return True
    else:
        return False


def is_text(value):
    if isinstance(value, text_type):
        return True
    else:
        return False


def is_integer(value):
    if isinstance(value, integer_types):
        return True
    else:
        return False