# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/ds9_region.py
# Compiled at: 2009-03-11 19:30:33
import os

def _fmtglobal(d):
    o = []
    for k, v in d.items():
        o.append('%s=%s' % (str(k), str(v)))

    return (' ').join(o)


class writer:

    def __init__(self, fd):
        self.globals = []
        self.regions = []
        self.fd = fd

    def header(self, d):
        self.globals.append('global ' + _fmtglobal(d))

    def text(self, x, y, text):
        self.regions.append('image;text(%g,%g) # text={%s}' % (
         x, y, text))

    def close(self):
        for g in self.globals:
            self.fd.writelines(g + '\n')

        for r in self.regions:
            self.fd.writelines(r + '\n')

        self.fd.flush()
        os.fsync(self.fd.fileno())
        self.fd = None
        return

    def __del__(self):
        if self.fd is not None:
            self.close()
        return