# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpfwd/next.py
# Compiled at: 2018-12-30 12:01:29


class Numbers(object):
    __module__ = __name__
    current = 0

    def getId(self):
        self.current += 1
        if self.current > 65535:
            self.current = 0
        return self.current


numbers = Numbers()
getId = numbers.getId