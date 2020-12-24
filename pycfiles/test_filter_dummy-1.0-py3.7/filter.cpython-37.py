# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test_filter_dummy/filter.py
# Compiled at: 2019-10-10 14:02:33
# Size of source mod 2**32: 227 bytes


class filtermanager:

    def __init__(self, a, b, c):
        self.a = int(a)
        self.b = int(b)
        self.c = int(c)

    def calc(self):
        print(self.a * self.b)

    def cald(self):
        print(self.b / self.c)