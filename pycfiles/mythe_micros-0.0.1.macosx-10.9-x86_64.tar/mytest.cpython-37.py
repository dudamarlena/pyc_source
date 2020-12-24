# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/mythe_micros/mytest.py
# Compiled at: 2019-12-22 10:32:25
# Size of source mod 2**32: 158 bytes


def mysum(*values):
    s = 0
    for v in values:
        i = int(v)
        s += i

    print(s)


def output():
    print('http://someurl')