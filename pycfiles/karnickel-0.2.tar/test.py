# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gbr/devel/karnickel/example/test.py
# Compiled at: 2010-05-01 13:57:21
from example.macros.__macros__ import add, assign, custom_loop

def usage_expr():
    return add(1, 2) + add(3, 4) + add(add(3, 4), 5)


def usage_block():
    assign(j, 1)
    return j


def usage_3():
    with custom_loop(10):
        print 'loop continues...'