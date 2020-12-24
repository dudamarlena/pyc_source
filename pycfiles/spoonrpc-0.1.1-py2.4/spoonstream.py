# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/spoon/spoonstream.py
# Compiled at: 2006-11-27 19:03:57
import ber, StringIO, zlib

class SocketFile(object):
    """
    Simple wrapper around a socket like object that pretends to be a file.
    Albeit one that can't seek or tell for obvious reasons.
    """
    __module__ = __name__

    def __init__(self, sock):
        self.sock = sock

    def read(self, cnt=1):
        return self.sock.recv(cnt)

    def write(self, data):
        return self.sock.send(data)

    def close(self):
        self.sock.close()


class SpoonStream(object):
    """
    SpoonStream implements an object stream.
    This will take either a file like object or a socket like object
    """
    __module__ = __name__

    def __init__(self, fd, compress=False):
        self.compress = compress
        self.realfd = fd
        if hasattr(fd, 'write') and hasattr(fd, 'read'):
            self.fd = fd
        else:
            self.fd = SocketFile(fd)
        self.buffer = StringIO.StringIO()

    def read(self, cnt=None):
        return ber.BERStream(self.fd).next()

    def recv(self, cnt=None):
        return self.read()

    def write(self, obj):
        ber.BERStream(self.buffer).add(obj, self.compress)
        self.fd.write(self.buffer.getvalue())
        self.buffer.truncate(0)

    def send(self, obj):
        self.write(obj)

    def close(self):
        self.realfd.close()