# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/foundation/bufferedwriter.py
# Compiled at: 2012-10-12 07:02:39
from StringIO import StringIO

class BufferedWriter:

    def __init__(self, w, debug=True):
        self.w = w
        self.buf = StringIO('')
        self.debug = debug

    def write(self, s):
        if self.debug:
            sys.stderr.write(s)
        self.buf.write(s)

    def flush(self):
        self.w.write(self.buf.getvalue().encode('utf-8'))
        self.w.flush()

    def getSize(self):
        return len(self.buf.getvalue().encode('utf-8'))

    def getValue(self):
        return self.buf.getvalue().encode('utf-8')

    def __del__(self):
        self.buf.close()
        self.buf = None
        self.w = None
        return