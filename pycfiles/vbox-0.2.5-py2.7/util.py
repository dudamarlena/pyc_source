# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vbox\vm\util.py
# Compiled at: 2013-03-15 12:05:06
"""Utility functions."""

def mutating(fn):

    def __wrapper__(self, *args, **kwargs):
        try:
            return fn(self, *args, **kwargs)
        finally:
            self.refresh()

    return __wrapper__


def controlCb(name):

    def __callback__(self, value):
        self.control({name: value}, quiet=True)

    return __callback__