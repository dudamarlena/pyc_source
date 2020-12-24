# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\shu\PycharmProjects\py34\constant-project\constant\pkg\sixmini.py
# Compiled at: 2017-04-06 15:23:44
# Size of source mod 2**32: 1027 bytes
__doc__ = '\nThis is a minimized six model\n'
import sys, types
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    string_types = (
     str,)
    integer_types = (int,)
    class_types = (type,)
    text_type = str
    binary_type = bytes
    MAXSIZE = sys.maxsize
else:
    string_types = (
     basestring,)
    integer_types = (int, long)
    class_types = (type, types.ClassType)
    text_type = unicode
    binary_type = str
if sys.platform.startswith('java'):
    MAXSIZE = int(2147483647)
else:

    class X(object):

        def __len__(self):
            return 2147483648


    try:
        len(X())
    except OverflowError:
        MAXSIZE = int(2147483647)
    else:
        MAXSIZE = int(9223372036854775807)
    del X