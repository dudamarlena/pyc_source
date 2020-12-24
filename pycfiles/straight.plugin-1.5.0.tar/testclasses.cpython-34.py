# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: test-packages/class-test-plugins/testplugin/testclasses.py
# Compiled at: 2016-02-03 22:21:36
# Size of source mod 2**32: 148 bytes


class A(object):

    class __plugin__:
        priority = 0.5


class B(object):

    class __plugin__:
        priority = 1.0


class A1(A):
    pass