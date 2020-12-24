# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/testingpro/__init__.py
# Compiled at: 2019-03-07 04:52:49


class test(object):

    def add(self, a, b):
        z = a + b
        print z


x = test()
x.add(10, 20)