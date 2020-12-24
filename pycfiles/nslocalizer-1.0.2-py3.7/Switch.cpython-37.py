# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nslocalizer/Helpers/Switch.py
# Compiled at: 2019-02-23 14:43:18
# Size of source mod 2**32: 2253 bytes


class Switch(object):

    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        result = False
        if not self.fall:
            if not args:
                result = True
        elif self.value in args:
            self.fall = True
            result = True
        return result