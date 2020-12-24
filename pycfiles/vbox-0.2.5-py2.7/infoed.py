# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vbox\util\infoed.py
# Compiled at: 2013-03-15 12:05:06


def infoed(fn):

    def __wrapper__(self, *args, **kwargs):
        self.info
        return fn(self, *args, **kwargs)

    return property(__wrapper__)