# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/msoucy/.virtualenv/fuf/lib/python2.7/site-packages/fuf/selfcall.py
# Compiled at: 2014-09-23 17:45:03
"""
selfcall.py
Matt Soucy

Simple decorators related to "self-calling" things
"""

def mainfunc(func):
    if func.__module__ == '__main__':
        func()
    return func


def SelfInit(*args, **kwargs):
    if len(args) == 1 and not kwargs and hasattr(args[0], '__call__'):
        return SelfInit()(args[0])

    def _wrap(func):
        return func(*args, **kwargs)

    return _wrap