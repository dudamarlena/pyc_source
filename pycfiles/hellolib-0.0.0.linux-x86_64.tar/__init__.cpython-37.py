# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/hello/__init__.py
# Compiled at: 2019-09-18 20:39:22
# Size of source mod 2**32: 96 bytes


def say_hello(name=None):
    if name:
        return 'hello, %s!' % name
    return 'hello!'