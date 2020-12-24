# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennings/Projects/community/python/rosie/adapt23.py
# Compiled at: 2019-03-13 09:48:34
import sys
PYTHON_VERSION = None
if sys.version_info.major == 2:
    PYTHON_VERSION = 2
    str23 = lambda s: str(s)
    bytes23 = lambda s: bytes(s)
    zip23 = zip
    map23 = map
    filter23 = filter
elif sys.version_info.major == 3:
    PYTHON_VERSION = 3

    def bytes23(s):
        if isinstance(s, str):
            return bytes(s, encoding='UTF-8')
        if isinstance(s, bytes):
            return s
        raise ValueError('obj not str or bytes: ' + repr(type(s)))


    def str23(s):
        if isinstance(s, str):
            return s
        if isinstance(s, bytes):
            return str(s, encoding='UTF-8')
        raise ValueError('obj not str or bytes: ' + repr(type(s)))


    def zip23(*args):
        return list(zip(*args))


    def map23(fn, *args):
        return list(map(fn, *args))


    def filter23(fn, *args):
        return list(filter(fn, *args))


else:
    raise RuntimeError('Unexpected python major version')