# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /thrift/transport/TTransport.py
# Compiled at: 2018-09-11 21:54:05
# Size of source mod 2**32: 13160 bytes
from struct import pack, unpack
from thrift.Thrift import TException
from ..compat import BufferIO

class TTransportException(TException):
    __doc__ = 'Custom Transport Exception class'
    UNKNOWN = 0
    NOT_OPEN = 1
    ALREADY_OPEN = 2
    TIMED_OUT = 3
    END_OF_FILE = 4
    NEGATIVE_SIZE = 5
    SIZE_LIMIT = 6
    INVALID_CLIENT_TYPE = 7

    def __init__(self, type=UNKNOWN, message=None):
        TException.__init__(self, message)
        self.type = type


class TTransportBase(object):
    __doc__ = 'Base class for Thrift transport layer.'

    def isOpen(self):
        pass

    def open(self):
        pass

    def close(self):
        pass

    def read(self, sz):
        pass

    def readAll(self, sz):
        buff = b''
        have = 0
        while have < sz:
            chunk = self.read(sz - have)
            chunkLen = len(chunk)
            have += chunkLen
            buff += chunk
            if chunkLen == 0:
                raise EOFError()

        return buff

    def write(self, buf):
        pass

    def flush(self):
        pass


class CReadableTransport(object):
    __doc__ = 'base class for transports that are readable from C'

    @property
    def cstringio_buf(self):
        """A cStringIO buffer that contains the current chunk we are reading."""
        pass

    def cstringio_refill(self, partialread, reqlen):
        """Refills cstringio_buf.

        Returns the currently used buffer (which can but need not be the same as
        the old cstringio_buf). partialread is what the C code has read from the
        buffer, and should be inserted into the buffer before any more reads.  The
        return value must be a new, not borrowed reference.  Something along the
        lines of self._buf should be fine.

        If reqlen bytes can't be read, throw EOFError.
        """
        pass


class TServerTransportBase(object):
    __doc__ = 'Base class for Thrift server transports.'

    def listen(self):
        pass

    def accept(self):
        pass

    def close(self):
        pass


class TTransportFactoryBase(object):
    __doc__ = 'Base class for a Transport Factory'

    def getTransport(self, trans):
        return trans


class TBufferedTransportFactory(object):
    __doc__ = 'Factory transport that builds buffered transports'

    def getTransport(self, trans):
        buffered = TBufferedTransport(trans)
        return buffered


class TBufferedTransport(TTransportBase, CReadableTransport):
    __doc__ = 'Class that wraps another transport and buffers its I/O.\n\n    The implementation uses a (configurable) fixed-size read buffer\n    but buffers all writes until a flush is performed.\n    '
    DEFAULT_BUFFER = 4096

    def __init__(self, trans, rbuf_size=DEFAULT_BUFFER):
        self._TBufferedTransport__trans = trans
        self._TBufferedTransport__wbuf = BufferIO()
        self._TBufferedTransport__rbuf = BufferIO(b'')
        self._TBufferedTransport__rbuf_size = rbuf_size

    def isOpen(self):
        return self._TBufferedTransport__trans.isOpen()

    def open(self):
        return self._TBufferedTransport__trans.open()

    def close(self):
        return self._TBufferedTransport__trans.close()

    def read(self, sz):
        ret = self._TBufferedTransport__rbuf.read(sz)
        if len(ret) != 0:
            return ret
        else:
            self._TBufferedTransport__rbuf = BufferIO(self._TBufferedTransport__trans.read(max(sz, self._TBufferedTransport__rbuf_size)))
            return self._TBufferedTransport__rbuf.read(sz)

    def write(self, buf):
        try:
            self._TBufferedTransport__wbuf.write(buf)
        except Exception as e:
            self._TBufferedTransport__wbuf = BufferIO()
            raise e

    def flush(self):
        out = self._TBufferedTransport__wbuf.getvalue()
        self._TBufferedTransport__wbuf = BufferIO()
        self._TBufferedTransport__trans.write(out)
        self._TBufferedTransport__trans.flush()

    @property
    def cstringio_buf(self):
        return self._TBufferedTransport__rbuf

    def cstringio_refill(self, partialread, reqlen):
        retstring = partialread
        if reqlen < self._TBufferedTransport__rbuf_size:
            retstring += self._TBufferedTransport__trans.read(self._TBufferedTransport__rbuf_size)
        if len(retstring) < reqlen:
            retstring += self._TBufferedTransport__trans.readAll(reqlen - len(retstring))
        self._TBufferedTransport__rbuf = BufferIO(retstring)
        return self._TBufferedTransport__rbuf


class TMemoryBuffer(TTransportBase, CReadableTransport):
    __doc__ = 'Wraps a cBytesIO object as a TTransport.\n\n    NOTE: Unlike the C++ version of this class, you cannot write to it\n          then immediately read from it.  If you want to read from a\n          TMemoryBuffer, you must either pass a string to the constructor.\n    TODO(dreiss): Make this work like the C++ version.\n    '

    def __init__(self, value=None, offset=0):
        """value -- a value to read from for stringio

        If value is set, this will be a transport for reading,
        otherwise, it is for writing"""
        if value is not None:
            self._buffer = BufferIO(value)
        else:
            self._buffer = BufferIO()
        if offset:
            self._buffer.seek(offset)

    def isOpen(self):
        return not self._buffer.closed

    def open(self):
        pass

    def close(self):
        self._buffer.close()

    def read(self, sz):
        return self._buffer.read(sz)

    def write(self, buf):
        self._buffer.write(buf)

    def flush(self):
        pass

    def getvalue(self):
        return self._buffer.getvalue()

    @property
    def cstringio_buf(self):
        return self._buffer

    def cstringio_refill(self, partialread, reqlen):
        raise EOFError()


class TFramedTransportFactory(object):
    __doc__ = 'Factory transport that builds framed transports'

    def getTransport(self, trans):
        framed = TFramedTransport(trans)
        return framed


class TFramedTransport(TTransportBase, CReadableTransport):
    __doc__ = 'Class that wraps another transport and frames its I/O when writing.'

    def __init__(self, trans):
        self._TFramedTransport__trans = trans
        self._TFramedTransport__rbuf = BufferIO(b'')
        self._TFramedTransport__wbuf = BufferIO()

    def isOpen(self):
        return self._TFramedTransport__trans.isOpen()

    def open(self):
        return self._TFramedTransport__trans.open()

    def close(self):
        return self._TFramedTransport__trans.close()

    def read(self, sz):
        ret = self._TFramedTransport__rbuf.read(sz)
        if len(ret) != 0:
            return ret
        else:
            self.readFrame()
            return self._TFramedTransport__rbuf.read(sz)

    def readFrame(self):
        buff = self._TFramedTransport__trans.readAll(4)
        sz, = unpack('!i', buff)
        self._TFramedTransport__rbuf = BufferIO(self._TFramedTransport__trans.readAll(sz))

    def write(self, buf):
        self._TFramedTransport__wbuf.write(buf)

    def flush(self):
        wout = self._TFramedTransport__wbuf.getvalue()
        wsz = len(wout)
        self._TFramedTransport__wbuf = BufferIO()
        buf = pack('!i', wsz) + wout
        self._TFramedTransport__trans.write(buf)
        self._TFramedTransport__trans.flush()

    @property
    def cstringio_buf(self):
        return self._TFramedTransport__rbuf

    def cstringio_refill(self, prefix, reqlen):
        while len(prefix) < reqlen:
            self.readFrame()
            prefix += self._TFramedTransport__rbuf.getvalue()

        self._TFramedTransport__rbuf = BufferIO(prefix)
        return self._TFramedTransport__rbuf


class TFileObjectTransport(TTransportBase):
    __doc__ = 'Wraps a file-like object to make it work as a Thrift transport.'

    def __init__(self, fileobj):
        self.fileobj = fileobj

    def isOpen(self):
        return True

    def close(self):
        self.fileobj.close()

    def read(self, sz):
        return self.fileobj.read(sz)

    def write(self, buf):
        self.fileobj.write(buf)

    def flush(self):
        self.fileobj.flush()


class TSaslClientTransport(TTransportBase, CReadableTransport):
    __doc__ = '\n    SASL transport\n    '
    START = 1
    OK = 2
    BAD = 3
    ERROR = 4
    COMPLETE = 5

    def __init__(self, transport, host, service, mechanism='GSSAPI', **sasl_kwargs):
        """
        transport: an underlying transport to use, typically just a TSocket
        host: the name of the server, from a SASL perspective
        service: the name of the server's service, from a SASL perspective
        mechanism: the name of the preferred mechanism to use

        All other kwargs will be passed to the puresasl.client.SASLClient
        constructor.
        """
        from puresasl.client import SASLClient
        self.transport = transport
        self.sasl = SASLClient(host, service, mechanism, **sasl_kwargs)
        self._TSaslClientTransport__wbuf = BufferIO()
        self._TSaslClientTransport__rbuf = BufferIO(b'')

    def open(self):
        if not self.transport.isOpen():
            self.transport.open()
        self.send_sasl_msg(self.START, self.sasl.mechanism)
        self.send_sasl_msg(self.OK, self.sasl.process())
        while True:
            status, challenge = self.recv_sasl_msg()
            if status == self.OK:
                self.send_sasl_msg(self.OK, self.sasl.process(challenge))
            else:
                if status == self.COMPLETE:
                    if not self.sasl.complete:
                        raise TTransportException(TTransportException.NOT_OPEN, 'The server erroneously indicated that SASL negotiation was complete')
                    else:
                        break
                else:
                    raise TTransportException(TTransportException.NOT_OPEN, 'Bad SASL negotiation status: %d (%s)' % (
                     status, challenge))

    def send_sasl_msg(self, status, body):
        header = pack('>BI', status, len(body))
        self.transport.write(header + body)
        self.transport.flush()

    def recv_sasl_msg(self):
        header = self.transport.readAll(5)
        status, length = unpack('>BI', header)
        if length > 0:
            payload = self.transport.readAll(length)
        else:
            payload = ''
        return (
         status, payload)

    def write(self, data):
        self._TSaslClientTransport__wbuf.write(data)

    def flush(self):
        data = self._TSaslClientTransport__wbuf.getvalue()
        encoded = self.sasl.wrap(data)
        self.transport.write(''.join((pack('!i', len(encoded)), encoded)))
        self.transport.flush()
        self._TSaslClientTransport__wbuf = BufferIO()

    def read(self, sz):
        ret = self._TSaslClientTransport__rbuf.read(sz)
        if len(ret) != 0:
            return ret
        else:
            self._read_frame()
            return self._TSaslClientTransport__rbuf.read(sz)

    def _read_frame(self):
        header = self.transport.readAll(4)
        length, = unpack('!i', header)
        encoded = self.transport.readAll(length)
        self._TSaslClientTransport__rbuf = BufferIO(self.sasl.unwrap(encoded))

    def close(self):
        self.sasl.dispose()
        self.transport.close()

    @property
    def cstringio_buf(self):
        return self._TSaslClientTransport__rbuf

    def cstringio_refill(self, prefix, reqlen):
        while len(prefix) < reqlen:
            self._read_frame()
            prefix += self._TSaslClientTransport__rbuf.getvalue()

        self._TSaslClientTransport__rbuf = BufferIO(prefix)
        return self._TSaslClientTransport__rbuf