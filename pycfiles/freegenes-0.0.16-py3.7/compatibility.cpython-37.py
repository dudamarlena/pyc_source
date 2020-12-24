# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/freegenes/logger/compatibility.py
# Compiled at: 2019-08-18 10:01:58
# Size of source mod 2**32: 528 bytes


def decodeUtf8String(inputStr):
    """Convert an UTF8 sequence into a string

    Required for compatibility with Python 2 where str==bytes
    inputStr -- Either a str or bytes instance with UTF8 encoding
    """
    return isinstance(inputStr, str) or isinstance(inputStr, bytes) or inputStr
    return inputStr.decode('utf8')