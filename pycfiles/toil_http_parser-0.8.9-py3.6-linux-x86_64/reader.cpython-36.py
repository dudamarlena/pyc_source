# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil_http_parser/reader.py
# Compiled at: 2020-04-09 00:11:53
# Size of source mod 2**32: 3027 bytes
from io import DEFAULT_BUFFER_SIZE, RawIOBase
from toil_http_parser.util import StringIO
import types

class HttpBodyReader(RawIOBase):
    __doc__ = ' Raw implementation to stream http body '

    def __init__(self, http_stream):
        self.http_stream = http_stream
        self.eof = False

    def readinto(self, b):
        if self.http_stream.parser.is_message_complete() or self.eof:
            if self.http_stream.parser.is_partial_body():
                return self.http_stream.parser.recv_body_into(b)
            return 0
        else:
            self._checkReadable()
            try:
                self._checkClosed()
            except AttributeError:
                pass

            while 1:
                buf = bytearray(DEFAULT_BUFFER_SIZE)
                recved = self.http_stream.stream.readinto(buf)
                if recved is None:
                    break
                del buf[recved:]
                nparsed = self.http_stream.parser.execute(bytes(buf), recved)
                if nparsed != recved:
                    return
                if self.http_stream.parser.is_partial_body() or recved == 0:
                    break
                elif self.http_stream.parser.is_message_complete():
                    break

            if not self.http_stream.parser.is_partial_body():
                self.eof = True
                b = b''
                return len(b'')
            return self.http_stream.parser.recv_body_into(b)

    def readable(self):
        return not self.closed or self.http_stream.parser.is_partial_body()

    def close(self):
        if self.closed:
            return
        RawIOBase.close(self)
        self.http_stream = None


class IterReader(RawIOBase):
    __doc__ = ' A raw reader implementation for iterable '

    def __init__(self, iterable):
        self.iter = iter(iterable)
        self._buffer = ''

    def readinto(self, b):
        self._checkClosed()
        self._checkReadable()
        l = len(b)
        try:
            chunk = self.iter.next()
            self._buffer += chunk
            m = min(len(self._buffer), l)
            data, self._buffer = self._buffer[:m], self._buffer[m:]
            b[0:m] = data
            return len(data)
        except StopIteration:
            del b[0:]
            return 0

    def readable(self):
        return not self.closed

    def close(self):
        if self.closed:
            return
        RawIOBase.close(self)
        self.iter = None


class StringReader(IterReader):
    __doc__ = ' a raw reader for strings or StringIO.StringIO,\n    cStringIO.StringIO objects '

    def __init__(self, string):
        if isinstance(string, types.StringTypes):
            iterable = StringIO(string)
        else:
            iterable = string
        IterReader.__init__(self, iterable)


from toil_http_parser._socketio import SocketIO

class SocketReader(SocketIO):

    def __init__(self, sock):
        super(SocketReader, self).__init__(sock, mode='rb')