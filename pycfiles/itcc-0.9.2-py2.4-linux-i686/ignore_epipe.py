# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/core/ignore_epipe.py
# Compiled at: 2008-04-20 13:19:45
import errno

class IgnoreEpipe(object):
    __module__ = __name__

    def __init__(self, ofile):
        self.ofile = ofile

    def write(self, str):
        try:
            self.ofile.write(str)
        except IOError, e:
            if e.errno != errno.EPIPE:
                raise

    def flush(self):
        try:
            self.ofile.flush()
        except IOError, e:
            if e.errno != errno.EPIPE:
                raise