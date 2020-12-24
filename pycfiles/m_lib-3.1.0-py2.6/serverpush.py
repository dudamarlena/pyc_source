# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/net/www/serverpush.py
# Compiled at: 2016-07-25 10:38:46
"""Server Push"""
import sys, mimetools

class ServerPush:

    def __init__(self, out=sys.stdout):
        self.out = out
        self.output = out.write
        self.boundary = mimetools.choose_boundary()

    def start(self):
        self.output('Content-type: multipart/x-mixed-replace;boundary=%s\n\n' % self.boundary)

    def next(self, content_type='text/html'):
        self.output('--%s\nContent-type: %s\n' % (self.boundary, content_type))

    def stop(self):
        self.output('--%s--' % self.boundary)