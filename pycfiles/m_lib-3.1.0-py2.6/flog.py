# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/flog.py
# Compiled at: 2016-07-25 10:38:46
"""File logger"""
from time import *

class FLog:

    def __init__(self, f, overwrite=0, timeformat='%a %d %b %Y %T'):
        if type(f) == type(''):
            if overwrite:
                mode = 'w'
            else:
                mode = 'a'
            self.outfile = open(f, mode)
        else:
            self.outfile = f
        self.f = f
        self.timeformat = timeformat

    def __del__(self):
        self.close()

    def close(self):
        if type(self.f) == type(''):
            self.outfile.close()

    def log(self, str):
        self.outfile.write('%s %s\n' % (strftime(self.timeformat, localtime(time())), str))

    __call__ = log

    def flush(self):
        self.outfile.flush()


def makelog(f):
    return FLog(f, 1)


def openlog(f):
    return FLog(f)


def test():
    log = makelog('test.log')
    log.log('Log opened')
    log('Log closed')
    log.close()


if __name__ == '__main__':
    test()