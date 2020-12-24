# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/gunicorn/gunicorn/http/unreader.py
# Compiled at: 2019-02-14 00:35:18
import os
from gunicorn import six

class Unreader(object):

    def __init__(self):
        self.buf = six.BytesIO()

    def chunk(self):
        raise NotImplementedError()

    def read(self, size=None):
        if size is not None and not isinstance(size, six.integer_types):
            raise TypeError('size parameter must be an int or long.')
        if size is not None:
            if size == 0:
                return ''
            if size < 0:
                size = None
        self.buf.seek(0, os.SEEK_END)
        if size is None and self.buf.tell():
            ret = self.buf.getvalue()
            self.buf = six.BytesIO()
            return ret
        else:
            if size is None:
                d = self.chunk()
                return d
            while self.buf.tell() < size:
                chunk = self.chunk()
                if not chunk:
                    ret = self.buf.getvalue()
                    self.buf = six.BytesIO()
                    return ret
                self.buf.write(chunk)

            data = self.buf.getvalue()
            self.buf = six.BytesIO()
            self.buf.write(data[size:])
            return data[:size]

    def unread(self, data):
        self.buf.seek(0, os.SEEK_END)
        self.buf.write(data)


class SocketUnreader(Unreader):

    def __init__(self, sock, max_chunk=8192):
        super(SocketUnreader, self).__init__()
        self.sock = sock
        self.mxchunk = max_chunk

    def chunk(self):
        return self.sock.recv(self.mxchunk)


class IterUnreader(Unreader):

    def __init__(self, iterable):
        super(IterUnreader, self).__init__()
        self.iter = iter(iterable)

    def chunk(self):
        if not self.iter:
            return ''
        else:
            try:
                return six.next(self.iter)
            except StopIteration:
                self.iter = None
                return ''

            return