# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/decorators/formatters.py
# Compiled at: 2019-04-02 16:28:52
# Size of source mod 2**32: 147 bytes


def formatter(name=None):

    def decorate(func):
        func._formatter = name
        return func

    return decorate