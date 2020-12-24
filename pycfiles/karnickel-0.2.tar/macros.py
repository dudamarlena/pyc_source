# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gbr/devel/karnickel/example/macros.py
# Compiled at: 2010-05-01 10:28:54
from karnickel import macro

@macro
def add(i, j):
    i + j


@macro
def assign(n, v):
    n = v


@macro
def custom_loop(i):
    for __x in range(i):
        print __x
        if __x < i - 1:
            __body__