# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-03p63p8r/redis/redis/connection.py
# Compiled at: 2020-04-05 04:25:10
# Size of source mod 2**32: 54334 bytes
from __future__ import unicode_literals
from distutils.version import StrictVersion
from itertools import chain
from time import time
import errno, io, os, socket, sys, threading, warnings
from redis._compat import xrange, imap, byte_to_chr, unicode, long, nativestr, basestring, iteritems, LifoQueue, Empty, Full, urlparse, parse_qs, recv, recv_into, unquote, BlockingIOError, sendall, shutdown, ssl_wrap_socket
from redis.exceptions import AuthenticationError, AuthenticationWrongNumberOfArgsError, BusyLoadingError, ChildDeadlockedError, ConnectionError, DataError, ExecAbortError, InvalidResponse, NoPermissionError, NoScriptError, ReadOnlyError, RedisError, ResponseError, TimeoutError
from redis.utils import HIREDIS_AVAILABLE
try:
    import ssl
    ssl_available = True
except ImportError:
    ssl_available = False
else:
    NONBLOCKING_EXCEPTION_ERROR_NUMBERS = {BlockingIOError: errno.EWOULDBLOCK}
    if ssl_available:
        if hasattr(ssl, 'SSLWantReadError'):
            NONBLOCKING_EXCEPTION_ERROR_NUMBERS[ssl.SSLWantReadError] = 2
            NONBLOCKING_EXCEPTION_ERROR_NUMBERS[ssl.SSLWantWriteError] = 2
        else:
            NONBLOCKING_EXCEPTION_ERROR_NUMBERS[ssl.SSLError] = 2
    if socket.error not in NONBLOCKING_EXCEPTION_ERROR_NUMBERS:
        NONBLOCKING_EXCEPTION_ERROR_NUMBERS[socket.error] = -999999
    else:
        NONBLOCKING_EXCEPTIONS = tuple(NONBLOCKING_EXCEPTION_ERROR_NUMBERS.keys())
        if HIREDIS_AVAILABLE:
            import hiredis
            hiredis_version = StrictVersion(hiredis.__version__)
            HIREDIS_SUPPORTS_CALLABLE_ERRORS = hiredis_version >= StrictVersion('0.1.3')
            HIREDIS_SUPPORTS_BYTE_BUFFER = hiredis_version >= StrictVersion('0.1.4')
            HIREDIS_SUPPORTS_ENCODING_ERRORS = hiredis_version >= StrictVersion('1.0.0')
            if not HIREDIS_SUPPORTS_BYTE_BUFFER:
                msg = "redis-py works best with hiredis >= 0.1.4. You're running hiredis %s. Please consider upgrading." % hiredis.__version__
                warnings.warn(msg)
            HIREDIS_USE_BYTE_BUFFER = True
            if not HIREDIS_SUPPORTS_BYTE_BUFFER:
                HIREDIS_USE_BYTE_BUFFER = False
            SYM_STAR = b'*'
            SYM_DOLLAR = b'$'
            SYM_CRLF = b'\r\n'
            SYM_EMPTY = b''
            SERVER_CLOSED_CONNECTION_ERROR = 'Connection closed by server.'
            SENTINEL = object()

            class Encoder(object):
                __doc__ = 'Encode strings to bytes and decode bytes to strings'

                def __init__(self, encoding, encoding_errors, decode_responses):
                    self.encoding = encoding
                    self.encoding_errors = encoding_errors
                    self.decode_responses = decode_responses

                def encode(self, value):
                    """Return a bytestring representation of the value"""
                    if isinstance(value, bytes):
                        return value
                        if isinstance(value, bool):
                            raise DataError("Invalid input of type: 'bool'. Convert to a bytes, string, int or float first.")
                    elif isinstance(value, float):
                        value = repr(value).encode()
                    else:
                        if isinstance(value, (int, long)):
                            value = str(value).encode()
                        else:
                            if not isinstance(value, basestring):
                                typename = type(value).__name__
                                raise DataError("Invalid input of type: '%s'. Convert to a bytes, string, int or float first." % typename)
                    if isinstance(value, unicode):
                        value = value.encode(self.encoding, self.encoding_errors)
                    return value

                def decode(self, value, force=False):
                    """Return a unicode string from the byte representation"""
                    if self.decode_responses or force:
                        if isinstance(value, bytes):
                            value = value.decode(self.encoding, self.encoding_errors)
                    return value


            class BaseParser(object):
                EXCEPTION_CLASSES = {'ERR':{'max number of clients reached':ConnectionError, 
                  'Client sent AUTH, but no password is set':AuthenticationError, 
                  'invalid password':AuthenticationError, 
                  "wrong number of arguments for 'auth' command":AuthenticationWrongNumberOfArgsError}, 
                 'EXECABORT':ExecAbortError, 
                 'LOADING':BusyLoadingError, 
                 'NOSCRIPT':NoScriptError, 
                 'READONLY':ReadOnlyError, 
                 'NOAUTH':AuthenticationError, 
                 'NOPERM':NoPermissionError}

                def parse_error(self, response):
                    """Parse an error response"""
                    error_code = response.split(' ')[0]
                    if error_code in self.EXCEPTION_CLASSES:
                        response = response[len(error_code) + 1:]
                        exception_class = self.EXCEPTION_CLASSES[error_code]
                        if isinstance(exception_class, dict):
                            exception_class = exception_class.get(response, ResponseError)
                        return exception_class(response)
                    return ResponseError(response)


            class SocketBuffer(object):

                def __init__(self, socket, socket_read_size, socket_timeout):
                    self._sock = socket
                    self.socket_read_size = socket_read_size
                    self.socket_timeout = socket_timeout
                    self._buffer = io.BytesIO()
                    self.bytes_written = 0
                    self.bytes_read = 0

                @property
                def length(self):
                    return self.bytes_written - self.bytes_read

                def _read_from_socket--- This code section failed: ---

 L. 179         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _sock
                4  STORE_FAST               'sock'

 L. 180         6  LOAD_FAST                'self'
                8  LOAD_ATTR                socket_read_size
               10  STORE_FAST               'socket_read_size'

 L. 181        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _buffer
               16  STORE_FAST               'buf'

 L. 182        18  LOAD_FAST                'buf'
               20  LOAD_METHOD              seek
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                bytes_written
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L. 183        30  LOAD_CONST               0
               32  STORE_FAST               'marker'

 L. 184        34  LOAD_FAST                'timeout'
               36  LOAD_GLOBAL              SENTINEL
               38  COMPARE_OP               is-not
               40  STORE_FAST               'custom_timeout'

 L. 186     42_44  SETUP_FINALLY       312  'to 312'
               46  SETUP_FINALLY       172  'to 172'

 L. 187        48  LOAD_FAST                'custom_timeout'
               50  POP_JUMP_IF_FALSE    62  'to 62'

 L. 188        52  LOAD_FAST                'sock'
               54  LOAD_METHOD              settimeout
               56  LOAD_FAST                'timeout'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          
             62_0  COME_FROM            50  '50'

 L. 190        62  LOAD_GLOBAL              recv
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                _sock
               68  LOAD_FAST                'socket_read_size'
               70  CALL_FUNCTION_2       2  ''
               72  STORE_FAST               'data'

 L. 192        74  LOAD_GLOBAL              isinstance
               76  LOAD_FAST                'data'
               78  LOAD_GLOBAL              bytes
               80  CALL_FUNCTION_2       2  ''
               82  POP_JUMP_IF_FALSE   104  'to 104'
               84  LOAD_GLOBAL              len
               86  LOAD_FAST                'data'
               88  CALL_FUNCTION_1       1  ''
               90  LOAD_CONST               0
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   104  'to 104'

 L. 193        96  LOAD_GLOBAL              ConnectionError
               98  LOAD_GLOBAL              SERVER_CLOSED_CONNECTION_ERROR
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            94  '94'
            104_1  COME_FROM            82  '82'

 L. 194       104  LOAD_FAST                'buf'
              106  LOAD_METHOD              write
              108  LOAD_FAST                'data'
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          

 L. 195       114  LOAD_GLOBAL              len
              116  LOAD_FAST                'data'
              118  CALL_FUNCTION_1       1  ''
              120  STORE_FAST               'data_length'

 L. 196       122  LOAD_FAST                'self'
              124  DUP_TOP          
              126  LOAD_ATTR                bytes_written
              128  LOAD_FAST                'data_length'
              130  INPLACE_ADD      
              132  ROT_TWO          
              134  STORE_ATTR               bytes_written

 L. 197       136  LOAD_FAST                'marker'
              138  LOAD_FAST                'data_length'
              140  INPLACE_ADD      
              142  STORE_FAST               'marker'

 L. 199       144  LOAD_FAST                'length'
              146  LOAD_CONST               None
              148  COMPARE_OP               is-not
              150  POP_JUMP_IF_FALSE   162  'to 162'
              152  LOAD_FAST                'length'
              154  LOAD_FAST                'marker'
              156  COMPARE_OP               >
              158  POP_JUMP_IF_FALSE   162  'to 162'

 L. 200       160  JUMP_BACK            62  'to 62'
            162_0  COME_FROM           158  '158'
            162_1  COME_FROM           150  '150'

 L. 201       162  POP_BLOCK        
              164  POP_BLOCK        
              166  CALL_FINALLY        312  'to 312'
              168  LOAD_CONST               True
              170  RETURN_VALUE     
            172_0  COME_FROM_FINALLY    46  '46'

 L. 202       172  DUP_TOP          
              174  LOAD_GLOBAL              socket
              176  LOAD_ATTR                timeout
              178  COMPARE_OP               exception-match
              180  POP_JUMP_IF_FALSE   210  'to 210'
              182  POP_TOP          
              184  POP_TOP          
              186  POP_TOP          

 L. 203       188  LOAD_FAST                'raise_on_timeout'
              190  POP_JUMP_IF_FALSE   200  'to 200'

 L. 204       192  LOAD_GLOBAL              TimeoutError
              194  LOAD_STR                 'Timeout reading from socket'
              196  CALL_FUNCTION_1       1  ''
              198  RAISE_VARARGS_1       1  'exception instance'
            200_0  COME_FROM           190  '190'

 L. 205       200  POP_EXCEPT       
              202  POP_BLOCK        
              204  CALL_FINALLY        312  'to 312'
              206  LOAD_CONST               False
              208  RETURN_VALUE     
            210_0  COME_FROM           180  '180'

 L. 206       210  DUP_TOP          
              212  LOAD_GLOBAL              NONBLOCKING_EXCEPTIONS
              214  COMPARE_OP               exception-match
          216_218  POP_JUMP_IF_FALSE   306  'to 306'
              220  POP_TOP          
              222  STORE_FAST               'ex'
              224  POP_TOP          
              226  SETUP_FINALLY       294  'to 294'

 L. 211       228  LOAD_GLOBAL              NONBLOCKING_EXCEPTION_ERROR_NUMBERS
              230  LOAD_METHOD              get
              232  LOAD_FAST                'ex'
              234  LOAD_ATTR                __class__
              236  LOAD_CONST               -1
              238  CALL_METHOD_2         2  ''
              240  STORE_FAST               'allowed'

 L. 212       242  LOAD_FAST                'raise_on_timeout'
          244_246  POP_JUMP_IF_TRUE    274  'to 274'
              248  LOAD_FAST                'ex'
              250  LOAD_ATTR                errno
              252  LOAD_FAST                'allowed'
              254  COMPARE_OP               ==
          256_258  POP_JUMP_IF_FALSE   274  'to 274'

 L. 213       260  POP_BLOCK        
              262  POP_EXCEPT       
              264  CALL_FINALLY        294  'to 294'
              266  POP_BLOCK        
              268  CALL_FINALLY        312  'to 312'
              270  LOAD_CONST               False
              272  RETURN_VALUE     
            274_0  COME_FROM           256  '256'
            274_1  COME_FROM           244  '244'

 L. 214       274  LOAD_GLOBAL              ConnectionError
              276  LOAD_STR                 'Error while reading from socket: %s'

 L. 215       278  LOAD_FAST                'ex'
              280  LOAD_ATTR                args
              282  BUILD_TUPLE_1         1 

 L. 214       284  BINARY_MODULO    
              286  CALL_FUNCTION_1       1  ''
              288  RAISE_VARARGS_1       1  'exception instance'
              290  POP_BLOCK        
              292  BEGIN_FINALLY    
            294_0  COME_FROM           264  '264'
            294_1  COME_FROM_FINALLY   226  '226'
              294  LOAD_CONST               None
              296  STORE_FAST               'ex'
              298  DELETE_FAST              'ex'
              300  END_FINALLY      
              302  POP_EXCEPT       
              304  JUMP_FORWARD        308  'to 308'
            306_0  COME_FROM           216  '216'
              306  END_FINALLY      
            308_0  COME_FROM           304  '304'
              308  POP_BLOCK        
              310  BEGIN_FINALLY    
            312_0  COME_FROM           268  '268'
            312_1  COME_FROM           204  '204'
            312_2  COME_FROM           166  '166'
            312_3  COME_FROM_FINALLY    42  '42'

 L. 217       312  LOAD_FAST                'custom_timeout'
          314_316  POP_JUMP_IF_FALSE   330  'to 330'

 L. 218       318  LOAD_FAST                'sock'
              320  LOAD_METHOD              settimeout
              322  LOAD_FAST                'self'
              324  LOAD_ATTR                socket_timeout
              326  CALL_METHOD_1         1  ''
              328  POP_TOP          
            330_0  COME_FROM           314  '314'
              330  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 164

                def can_read(self, timeout):
                    return bool(self.length) or self._read_from_socket(timeout=timeout, raise_on_timeout=False)

                def read(self, length):
                    length = length + 2
                    if length > self.length:
                        self._read_from_socket(length - self.length)
                    self._buffer.seek(self.bytes_read)
                    data = self._buffer.read(length)
                    self.bytes_read += len(data)
                    if self.bytes_read == self.bytes_written:
                        self.purge()
                    return data[:-2]

                def readline(self):
                    buf = self._buffer
                    buf.seek(self.bytes_read)
                    data = buf.readline()
                    while not data.endswith(SYM_CRLF):
                        self._read_from_socket()
                        buf.seek(self.bytes_read)
                        data = buf.readline()

                    self.bytes_read += len(data)
                    if self.bytes_read == self.bytes_written:
                        self.purge()
                    return data[:-2]

                def purge(self):
                    self._buffer.seek(0)
                    self._buffer.truncate()
                    self.bytes_written = 0
                    self.bytes_read = 0

                def close(self):
                    try:
                        self.purge()
                        self._buffer.close()
                    except Exception:
                        pass
                    else:
                        self._buffer = None
                        self._sock = None


            class PythonParser(BaseParser):
                __doc__ = 'Plain Python parsing class'

                def __init__(self, socket_read_size):
                    self.socket_read_size = socket_read_size
                    self.encoder = None
                    self._sock = None
                    self._buffer = None

                def __del__(self):
                    try:
                        self.on_disconnect()
                    except Exception:
                        pass

                def on_connect(self, connection):
                    """Called when the socket connects"""
                    self._sock = connection._sock
                    self._buffer = SocketBuffer(self._sock, self.socket_read_size, connection.socket_timeout)
                    self.encoder = connection.encoder

                def on_disconnect(self):
                    """Called when the socket disconnects"""
                    self._sock = None
                    if self._buffer is not None:
                        self._buffer.close()
                        self._buffer = None
                    self.encoder = None

                def can_read(self, timeout):
                    return self._buffer and self._buffer.can_read(timeout)

                def read_response(self):
                    response = self._buffer.readline()
                    if not response:
                        raise ConnectionError(SERVER_CLOSED_CONNECTION_ERROR)
                    else:
                        byte, response = byte_to_chr(response[0]), response[1:]
                        if byte not in ('-', '+', ':', '$', '*'):
                            raise InvalidResponse('Protocol Error: %s, %s' % (
                             str(byte), str(response)))
                        elif byte == '-':
                            response = nativestr(response)
                            error = self.parse_error(response)
                            if isinstance(error, ConnectionError):
                                raise error
                        else:
                            return error
                            if byte == '+':
                                pass
                            elif byte == ':':
                                response = long(response)
                            else:
                                if byte == '$':
                                    length = int(response)
                                    if length == -1:
                                        return
                                    response = self._buffer.read(length)
                                else:
                                    if byte == '*':
                                        length = int(response)
                                        if length == -1:
                                            return
                                        response = [self.read_response() for i in xrange(length)]
                    if isinstance(response, bytes):
                        response = self.encoder.decode(response)
                    return response


            class HiredisParser(BaseParser):
                __doc__ = 'Parser class for connections using Hiredis'

                def __init__(self, socket_read_size):
                    if not HIREDIS_AVAILABLE:
                        raise RedisError('Hiredis is not installed')
                    self.socket_read_size = socket_read_size
                    if HIREDIS_USE_BYTE_BUFFER:
                        self._buffer = bytearray(socket_read_size)

                def __del__(self):
                    try:
                        self.on_disconnect()
                    except Exception:
                        pass

                def on_connect(self, connection):
                    self._sock = connection._sock
                    self._socket_timeout = connection.socket_timeout
                    kwargs = {'protocolError':InvalidResponse, 
                     'replyError':self.parse_error}
                    if not HIREDIS_SUPPORTS_CALLABLE_ERRORS:
                        kwargs['replyError'] = ResponseError
                    if connection.encoder.decode_responses:
                        kwargs['encoding'] = connection.encoder.encoding
                    if HIREDIS_SUPPORTS_ENCODING_ERRORS:
                        kwargs['errors'] = connection.encoder.encoding_errors
                    self._reader = (hiredis.Reader)(**kwargs)
                    self._next_response = False

                def on_disconnect(self):
                    self._sock = None
                    self._reader = None
                    self._next_response = False

                def can_read(self, timeout):
                    if not self._reader:
                        raise ConnectionError(SERVER_CLOSED_CONNECTION_ERROR)
                    if self._next_response is False:
                        self._next_response = self._reader.gets()
                        if self._next_response is False:
                            return self.read_from_socket(timeout=timeout, raise_on_timeout=False)
                    return True

                def read_from_socket--- This code section failed: ---

 L. 414         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _sock
                4  STORE_FAST               'sock'

 L. 415         6  LOAD_FAST                'timeout'
                8  LOAD_GLOBAL              SENTINEL
               10  COMPARE_OP               is-not
               12  STORE_FAST               'custom_timeout'

 L. 416     14_16  SETUP_FINALLY       294  'to 294'
               18  SETUP_FINALLY       154  'to 154'

 L. 417        20  LOAD_FAST                'custom_timeout'
               22  POP_JUMP_IF_FALSE    34  'to 34'

 L. 418        24  LOAD_FAST                'sock'
               26  LOAD_METHOD              settimeout
               28  LOAD_FAST                'timeout'
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          
             34_0  COME_FROM            22  '22'

 L. 419        34  LOAD_GLOBAL              HIREDIS_USE_BYTE_BUFFER
               36  POP_JUMP_IF_FALSE    88  'to 88'

 L. 420        38  LOAD_GLOBAL              recv_into
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _sock
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _buffer
               48  CALL_FUNCTION_2       2  ''
               50  STORE_FAST               'bufflen'

 L. 421        52  LOAD_FAST                'bufflen'
               54  LOAD_CONST               0
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE    68  'to 68'

 L. 422        60  LOAD_GLOBAL              ConnectionError
               62  LOAD_GLOBAL              SERVER_CLOSED_CONNECTION_ERROR
               64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            58  '58'

 L. 423        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _reader
               72  LOAD_METHOD              feed
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                _buffer
               78  LOAD_CONST               0
               80  LOAD_FAST                'bufflen'
               82  CALL_METHOD_3         3  ''
               84  POP_TOP          
               86  JUMP_FORWARD        144  'to 144'
             88_0  COME_FROM            36  '36'

 L. 425        88  LOAD_GLOBAL              recv
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                _sock
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                socket_read_size
               98  CALL_FUNCTION_2       2  ''
              100  STORE_FAST               'buffer'

 L. 427       102  LOAD_GLOBAL              isinstance
              104  LOAD_FAST                'buffer'
              106  LOAD_GLOBAL              bytes
              108  CALL_FUNCTION_2       2  ''
              110  POP_JUMP_IF_FALSE   124  'to 124'
              112  LOAD_GLOBAL              len
              114  LOAD_FAST                'buffer'
              116  CALL_FUNCTION_1       1  ''
              118  LOAD_CONST               0
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_FALSE   132  'to 132'
            124_0  COME_FROM           110  '110'

 L. 428       124  LOAD_GLOBAL              ConnectionError
              126  LOAD_GLOBAL              SERVER_CLOSED_CONNECTION_ERROR
              128  CALL_FUNCTION_1       1  ''
              130  RAISE_VARARGS_1       1  'exception instance'
            132_0  COME_FROM           122  '122'

 L. 429       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _reader
              136  LOAD_METHOD              feed
              138  LOAD_FAST                'buffer'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
            144_0  COME_FROM            86  '86'

 L. 432       144  POP_BLOCK        
              146  POP_BLOCK        
              148  CALL_FINALLY        294  'to 294'
              150  LOAD_CONST               True
              152  RETURN_VALUE     
            154_0  COME_FROM_FINALLY    18  '18'

 L. 433       154  DUP_TOP          
              156  LOAD_GLOBAL              socket
              158  LOAD_ATTR                timeout
              160  COMPARE_OP               exception-match
              162  POP_JUMP_IF_FALSE   192  'to 192'
              164  POP_TOP          
              166  POP_TOP          
              168  POP_TOP          

 L. 434       170  LOAD_FAST                'raise_on_timeout'
              172  POP_JUMP_IF_FALSE   182  'to 182'

 L. 435       174  LOAD_GLOBAL              TimeoutError
              176  LOAD_STR                 'Timeout reading from socket'
              178  CALL_FUNCTION_1       1  ''
              180  RAISE_VARARGS_1       1  'exception instance'
            182_0  COME_FROM           172  '172'

 L. 436       182  POP_EXCEPT       
              184  POP_BLOCK        
              186  CALL_FINALLY        294  'to 294'
              188  LOAD_CONST               False
              190  RETURN_VALUE     
            192_0  COME_FROM           162  '162'

 L. 437       192  DUP_TOP          
              194  LOAD_GLOBAL              NONBLOCKING_EXCEPTIONS
              196  COMPARE_OP               exception-match
          198_200  POP_JUMP_IF_FALSE   288  'to 288'
              202  POP_TOP          
              204  STORE_FAST               'ex'
              206  POP_TOP          
              208  SETUP_FINALLY       276  'to 276'

 L. 442       210  LOAD_GLOBAL              NONBLOCKING_EXCEPTION_ERROR_NUMBERS
              212  LOAD_METHOD              get
              214  LOAD_FAST                'ex'
              216  LOAD_ATTR                __class__
              218  LOAD_CONST               -1
              220  CALL_METHOD_2         2  ''
              222  STORE_FAST               'allowed'

 L. 443       224  LOAD_FAST                'raise_on_timeout'
          226_228  POP_JUMP_IF_TRUE    256  'to 256'
              230  LOAD_FAST                'ex'
              232  LOAD_ATTR                errno
              234  LOAD_FAST                'allowed'
              236  COMPARE_OP               ==
          238_240  POP_JUMP_IF_FALSE   256  'to 256'

 L. 444       242  POP_BLOCK        
              244  POP_EXCEPT       
              246  CALL_FINALLY        276  'to 276'
              248  POP_BLOCK        
              250  CALL_FINALLY        294  'to 294'
              252  LOAD_CONST               False
              254  RETURN_VALUE     
            256_0  COME_FROM           238  '238'
            256_1  COME_FROM           226  '226'

 L. 445       256  LOAD_GLOBAL              ConnectionError
              258  LOAD_STR                 'Error while reading from socket: %s'

 L. 446       260  LOAD_FAST                'ex'
              262  LOAD_ATTR                args
              264  BUILD_TUPLE_1         1 

 L. 445       266  BINARY_MODULO    
              268  CALL_FUNCTION_1       1  ''
              270  RAISE_VARARGS_1       1  'exception instance'
              272  POP_BLOCK        
              274  BEGIN_FINALLY    
            276_0  COME_FROM           246  '246'
            276_1  COME_FROM_FINALLY   208  '208'
              276  LOAD_CONST               None
              278  STORE_FAST               'ex'
              280  DELETE_FAST              'ex'
              282  END_FINALLY      
              284  POP_EXCEPT       
              286  JUMP_FORWARD        290  'to 290'
            288_0  COME_FROM           198  '198'
              288  END_FINALLY      
            290_0  COME_FROM           286  '286'
              290  POP_BLOCK        
              292  BEGIN_FINALLY    
            294_0  COME_FROM           250  '250'
            294_1  COME_FROM           186  '186'
            294_2  COME_FROM           148  '148'
            294_3  COME_FROM_FINALLY    14  '14'

 L. 448       294  LOAD_FAST                'custom_timeout'
          296_298  POP_JUMP_IF_FALSE   312  'to 312'

 L. 449       300  LOAD_FAST                'sock'
              302  LOAD_METHOD              settimeout
              304  LOAD_FAST                'self'
              306  LOAD_ATTR                _socket_timeout
              308  CALL_METHOD_1         1  ''
              310  POP_TOP          
            312_0  COME_FROM           296  '296'
              312  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 146

                def read_response(self):
                    if not self._reader:
                        raise ConnectionError(SERVER_CLOSED_CONNECTION_ERROR)
                    else:
                        if self._next_response is not False:
                            response = self._next_response
                            self._next_response = False
                            return response
                        response = self._reader.gets()
                        while True:
                            if response is False:
                                self.read_from_socket()
                                response = self._reader.gets()

                    if (HIREDIS_SUPPORTS_CALLABLE_ERRORS or isinstance)(response, ResponseError):
                        response = self.parse_error(response.args[0])
                    else:
                        if isinstance(response, list):
                            if response:
                                if isinstance(response[0], ResponseError):
                                    response[0] = self.parse_error(response[0].args[0])
                        elif isinstance(response, ConnectionError):
                            raise response
                        else:
                            if isinstance(response, list):
                                if response:
                                    if isinstance(response[0], ConnectionError):
                                        raise response[0]
                        return response


            if HIREDIS_AVAILABLE:
                DefaultParser = HiredisParser
        else:
            DefaultParser = PythonParser

    class Connection(object):
        __doc__ = 'Manages TCP communication to and from a Redis server'

        def __init__(self, host='localhost', port=6379, db=0, password=None, socket_timeout=None, socket_connect_timeout=None, socket_keepalive=False, socket_keepalive_options=None, socket_type=0, retry_on_timeout=False, encoding='utf-8', encoding_errors='strict', decode_responses=False, parser_class=DefaultParser, socket_read_size=65536, health_check_interval=0, client_name=None, username=None):
            self.pid = os.getpid()
            self.host = host
            self.port = int(port)
            self.db = db
            self.username = username
            self.client_name = client_name
            self.password = password
            self.socket_timeout = socket_timeout
            self.socket_connect_timeout = socket_connect_timeout or socket_timeout
            self.socket_keepalive = socket_keepalive
            self.socket_keepalive_options = socket_keepalive_options or {}
            self.socket_type = socket_type
            self.retry_on_timeout = retry_on_timeout
            self.health_check_interval = health_check_interval
            self.next_health_check = 0
            self.encoder = Encoder(encoding, encoding_errors, decode_responses)
            self._sock = None
            self._parser = parser_class(socket_read_size=socket_read_size)
            self._connect_callbacks = []
            self._buffer_cutoff = 6000

        def __repr__(self):
            repr_args = ','.join(['%s=%s' % (k, v) for k, v in self.repr_pieces()])
            return '%s<%s>' % (self.__class__.__name__, repr_args)

        def repr_pieces(self):
            pieces = [
             (
              'host', self.host),
             (
              'port', self.port),
             (
              'db', self.db)]
            if self.client_name:
                pieces.append(('client_name', self.client_name))
            return pieces

        def __del__(self):
            try:
                self.disconnect()
            except Exception:
                pass

        def register_connect_callback(self, callback):
            self._connect_callbacks.append(callback)

        def clear_connect_callbacks(self):
            self._connect_callbacks = []

        def connect(self):
            """Connects to the Redis server if not already connected"""
            if self._sock:
                return
            try:
                sock = self._connect()
            except socket.timeout:
                raise TimeoutError('Timeout connecting to server')
            except socket.error:
                e = sys.exc_info()[1]
                raise ConnectionError(self._error_message(e))
            else:
                self._sock = sock
                try:
                    self.on_connect()
                except RedisError:
                    self.disconnect()
                    raise
                else:
                    for callback in self._connect_callbacks:
                        callback(self)

        def _connect--- This code section failed: ---

 L. 577         0  LOAD_CONST               None
                2  STORE_FAST               'err'

 L. 578         4  LOAD_GLOBAL              socket
                6  LOAD_METHOD              getaddrinfo
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                host
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                port
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                socket_type

 L. 579        20  LOAD_GLOBAL              socket
               22  LOAD_ATTR                SOCK_STREAM

 L. 578        24  CALL_METHOD_4         4  ''
               26  GET_ITER         
               28  FOR_ITER            246  'to 246'
               30  STORE_FAST               'res'

 L. 580        32  LOAD_FAST                'res'
               34  UNPACK_SEQUENCE_5     5 
               36  STORE_FAST               'family'
               38  STORE_FAST               'socktype'
               40  STORE_FAST               'proto'
               42  STORE_FAST               'canonname'
               44  STORE_FAST               'socket_address'

 L. 581        46  LOAD_CONST               None
               48  STORE_FAST               'sock'

 L. 582        50  SETUP_FINALLY       188  'to 188'

 L. 583        52  LOAD_GLOBAL              socket
               54  LOAD_METHOD              socket
               56  LOAD_FAST                'family'
               58  LOAD_FAST                'socktype'
               60  LOAD_FAST                'proto'
               62  CALL_METHOD_3         3  ''
               64  STORE_FAST               'sock'

 L. 585        66  LOAD_FAST                'sock'
               68  LOAD_METHOD              setsockopt
               70  LOAD_GLOBAL              socket
               72  LOAD_ATTR                IPPROTO_TCP
               74  LOAD_GLOBAL              socket
               76  LOAD_ATTR                TCP_NODELAY
               78  LOAD_CONST               1
               80  CALL_METHOD_3         3  ''
               82  POP_TOP          

 L. 588        84  LOAD_FAST                'self'
               86  LOAD_ATTR                socket_keepalive
               88  POP_JUMP_IF_FALSE   144  'to 144'

 L. 589        90  LOAD_FAST                'sock'
               92  LOAD_METHOD              setsockopt
               94  LOAD_GLOBAL              socket
               96  LOAD_ATTR                SOL_SOCKET
               98  LOAD_GLOBAL              socket
              100  LOAD_ATTR                SO_KEEPALIVE
              102  LOAD_CONST               1
              104  CALL_METHOD_3         3  ''
              106  POP_TOP          

 L. 590       108  LOAD_GLOBAL              iteritems
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                socket_keepalive_options
              114  CALL_FUNCTION_1       1  ''
              116  GET_ITER         
              118  FOR_ITER            144  'to 144'
              120  UNPACK_SEQUENCE_2     2 
              122  STORE_FAST               'k'
              124  STORE_FAST               'v'

 L. 591       126  LOAD_FAST                'sock'
              128  LOAD_METHOD              setsockopt
              130  LOAD_GLOBAL              socket
              132  LOAD_ATTR                IPPROTO_TCP
              134  LOAD_FAST                'k'
              136  LOAD_FAST                'v'
              138  CALL_METHOD_3         3  ''
              140  POP_TOP          
              142  JUMP_BACK           118  'to 118'
            144_0  COME_FROM            88  '88'

 L. 594       144  LOAD_FAST                'sock'
              146  LOAD_METHOD              settimeout
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                socket_connect_timeout
              152  CALL_METHOD_1         1  ''
              154  POP_TOP          

 L. 597       156  LOAD_FAST                'sock'
              158  LOAD_METHOD              connect
              160  LOAD_FAST                'socket_address'
              162  CALL_METHOD_1         1  ''
              164  POP_TOP          

 L. 600       166  LOAD_FAST                'sock'
              168  LOAD_METHOD              settimeout
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                socket_timeout
              174  CALL_METHOD_1         1  ''
              176  POP_TOP          

 L. 601       178  LOAD_FAST                'sock'
              180  POP_BLOCK        
              182  ROT_TWO          
              184  POP_TOP          
              186  RETURN_VALUE     
            188_0  COME_FROM_FINALLY    50  '50'

 L. 603       188  DUP_TOP          
              190  LOAD_GLOBAL              socket
              192  LOAD_ATTR                error
              194  COMPARE_OP               exception-match
              196  POP_JUMP_IF_FALSE   242  'to 242'
              198  POP_TOP          
              200  STORE_FAST               '_'
              202  POP_TOP          
              204  SETUP_FINALLY       230  'to 230'

 L. 604       206  LOAD_FAST                '_'
              208  STORE_FAST               'err'

 L. 605       210  LOAD_FAST                'sock'
              212  LOAD_CONST               None
              214  COMPARE_OP               is-not
              216  POP_JUMP_IF_FALSE   226  'to 226'

 L. 606       218  LOAD_FAST                'sock'
              220  LOAD_METHOD              close
              222  CALL_METHOD_0         0  ''
              224  POP_TOP          
            226_0  COME_FROM           216  '216'
              226  POP_BLOCK        
              228  BEGIN_FINALLY    
            230_0  COME_FROM_FINALLY   204  '204'
              230  LOAD_CONST               None
              232  STORE_FAST               '_'
              234  DELETE_FAST              '_'
              236  END_FINALLY      
              238  POP_EXCEPT       
              240  JUMP_BACK            28  'to 28'
            242_0  COME_FROM           196  '196'
              242  END_FINALLY      
              244  JUMP_BACK            28  'to 28'

 L. 608       246  LOAD_FAST                'err'
              248  LOAD_CONST               None
              250  COMPARE_OP               is-not
          252_254  POP_JUMP_IF_FALSE   260  'to 260'

 L. 609       256  LOAD_FAST                'err'
              258  RAISE_VARARGS_1       1  'exception instance'
            260_0  COME_FROM           252  '252'

 L. 610       260  LOAD_GLOBAL              socket
              262  LOAD_METHOD              error
              264  LOAD_STR                 'socket.getaddrinfo returned an empty list'
              266  CALL_METHOD_1         1  ''
              268  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 182

        def _error_message(self, exception):
            if len(exception.args) == 1:
                return 'Error connecting to %s:%s. %s.' % (
                 self.host, self.port, exception.args[0])
            return 'Error %s connecting to %s:%s. %s.' % (
             exception.args[0], self.host, self.port, exception.args[1])

        def on_connect(self):
            """Initialize the connection, authenticate and select a database"""
            self._parser.on_connect(self)
            if self.username or self.password:
                if self.username:
                    auth_args = (
                     self.username, self.password or '')
                else:
                    auth_args = (
                     self.password,)
                (self.send_command)('AUTH', *auth_args, **{'check_health': False})
                try:
                    auth_response = self.read_response()
                except AuthenticationWrongNumberOfArgsError:
                    self.send_command('AUTH', (self.password), check_health=False)
                    auth_response = self.read_response()
                else:
                    if nativestr(auth_response) != 'OK':
                        raise AuthenticationError('Invalid Username or Password')
            if self.client_name:
                self.send_command'CLIENT''SETNAME'self.client_name
                if nativestr(self.read_response()) != 'OK':
                    raise ConnectionError('Error setting client name')
            if self.db:
                self.send_command('SELECT', self.db)
                if nativestr(self.read_response()) != 'OK':
                    raise ConnectionError('Invalid Database')

        def disconnect(self):
            """Disconnects from the Redis server"""
            self._parser.on_disconnect()
            if self._sock is None:
                return
            try:
                if os.getpid() == self.pid:
                    shutdown(self._sock, socket.SHUT_RDWR)
                self._sock.close()
            except socket.error:
                pass
            else:
                self._sock = None

        def check_health(self):
            """Check the health of the connection with a PING/PONG"""
            if self.health_check_interval:
                if time() > self.next_health_check:
                    try:
                        self.send_command('PING', check_health=False)
                        if nativestr(self.read_response()) != 'PONG':
                            raise ConnectionError('Bad response from PING health check')
                    except (ConnectionError, TimeoutError) as ex:
                        try:
                            self.disconnect()
                            self.send_command('PING', check_health=False)
                            if nativestr(self.read_response()) != 'PONG':
                                raise ConnectionError('Bad response from PING health check')
                        finally:
                            ex = None
                            del ex

        def send_packed_command(self, command, check_health=True):
            """Send an already packed command to the Redis server"""
            if not self._sock:
                self.connect()
            else:
                if check_health:
                    self.check_health()
                try:
                    if isinstance(command, str):
                        command = [
                         command]
                    for item in command:
                        sendall(self._sock, item)

                except socket.timeout:
                    self.disconnect()
                    raise TimeoutError('Timeout writing to socket')
                except socket.error:
                    e = sys.exc_info()[1]
                    self.disconnect()
                    if len(e.args) == 1:
                        errno, errmsg = 'UNKNOWN', e.args[0]
                    else:
                        errno = e.args[0]
                        errmsg = e.args[1]
                    raise ConnectionError('Error %s while writing to socket. %s.' % (
                     errno, errmsg))
                except:
                    self.disconnect()
                    raise

        def send_command(self, *args, **kwargs):
            """Pack and send a command to the Redis server"""
            self.send_packed_command((self.pack_command)(*args), check_health=(kwargs.get('check_health', True)))

        def can_read(self, timeout=0):
            """Poll the socket to see if there's data that can be read."""
            sock = self._sock
            if not sock:
                self.connect()
                sock = self._sock
            return self._parser.can_read(timeout)

        def read_response(self):
            """Read the response from a previously sent command"""
            try:
                response = self._parser.read_response()
            except socket.timeout:
                self.disconnect()
                raise TimeoutError('Timeout reading from %s:%s' % (
                 self.host, self.port))
            except socket.error:
                self.disconnect()
                e = sys.exc_info()[1]
                raise ConnectionError('Error while reading from %s:%s : %s' % (
                 self.host, self.port, e.args))
            except:
                self.disconnect()
                raise
            else:
                if self.health_check_interval:
                    self.next_health_check = time() + self.health_check_interval
                if isinstance(response, ResponseError):
                    raise response
                return response

        def pack_command(self, *args):
            """Pack a series of arguments into the Redis protocol"""
            output = []
            if isinstance(args[0], unicode):
                args = tuple(args[0].encode().split()) + args[1:]
            else:
                if b' ' in args[0]:
                    args = tuple(args[0].split()) + args[1:]
            buff = SYM_EMPTY.join((SYM_STAR, str(len(args)).encode(), SYM_CRLF))
            buffer_cutoff = self._buffer_cutoff
            for arg in imap(self.encoder.encode, args):
                arg_length = len(arg)
                if len(buff) > buffer_cutoff or arg_length > buffer_cutoff:
                    buff = SYM_EMPTY.join((
                     buff, SYM_DOLLAR, str(arg_length).encode(), SYM_CRLF))
                    output.append(buff)
                    output.append(arg)
                    buff = SYM_CRLF
                else:
                    buff = SYM_EMPTY.join((
                     buff, SYM_DOLLAR, str(arg_length).encode(),
                     SYM_CRLF, arg, SYM_CRLF))
            else:
                output.append(buff)
                return output

        def pack_commands(self, commands):
            """Pack multiple commands into the Redis protocol"""
            output = []
            pieces = []
            buffer_length = 0
            buffer_cutoff = self._buffer_cutoff
            for cmd in commands:
                for chunk in (self.pack_command)(*cmd):
                    chunklen = len(chunk)
                    if not buffer_length > buffer_cutoff:
                        if chunklen > buffer_cutoff:
                            output.append(SYM_EMPTY.join(pieces))
                            buffer_length = 0
                            pieces = []
                        if chunklen > self._buffer_cutoff:
                            output.append(chunk)
                        else:
                            pieces.append(chunk)
                            buffer_length += chunklen
                else:
                    if pieces:
                        output.append(SYM_EMPTY.join(pieces))
                    return output


    class SSLConnection(Connection):

        def __init__(self, ssl_keyfile=None, ssl_certfile=None, ssl_cert_reqs='required', ssl_ca_certs=None, ssl_check_hostname=False, **kwargs):
            if not ssl_available:
                raise RedisError("Python wasn't built with SSL support")
            else:
                (super(SSLConnection, self).__init__)(**kwargs)
                self.keyfile = ssl_keyfile
                self.certfile = ssl_certfile
                if ssl_cert_reqs is None:
                    ssl_cert_reqs = ssl.CERT_NONE
                else:
                    if isinstance(ssl_cert_reqs, basestring):
                        CERT_REQS = {'none':ssl.CERT_NONE,  'optional':ssl.CERT_OPTIONAL, 
                         'required':ssl.CERT_REQUIRED}
                        if ssl_cert_reqs not in CERT_REQS:
                            raise RedisError('Invalid SSL Certificate Requirements Flag: %s' % ssl_cert_reqs)
                        ssl_cert_reqs = CERT_REQS[ssl_cert_reqs]
            self.cert_reqs = ssl_cert_reqs
            self.ca_certs = ssl_ca_certs
            self.check_hostname = ssl_check_hostname

        def _connect(self):
            sock = super(SSLConnection, self)._connect()
            if hasattr(ssl, 'create_default_context'):
                context = ssl.create_default_context()
                context.check_hostname = self.check_hostname
                context.verify_mode = self.cert_reqs
                if self.certfile:
                    if self.keyfile:
                        context.load_cert_chain(certfile=(self.certfile), keyfile=(self.keyfile))
                if self.ca_certs:
                    context.load_verify_locations(self.ca_certs)
                sock = ssl_wrap_socket(context, sock, server_hostname=(self.host))
            else:
                sock = ssl_wrap_socket(ssl, sock,
                  cert_reqs=(self.cert_reqs),
                  keyfile=(self.keyfile),
                  certfile=(self.certfile),
                  ca_certs=(self.ca_certs))
            return sock


    class UnixDomainSocketConnection(Connection):

        def __init__(self, path='', db=0, username=None, password=None, socket_timeout=None, encoding='utf-8', encoding_errors='strict', decode_responses=False, retry_on_timeout=False, parser_class=DefaultParser, socket_read_size=65536, health_check_interval=0, client_name=None):
            self.pid = os.getpid()
            self.path = path
            self.db = db
            self.username = username
            self.client_name = client_name
            self.password = password
            self.socket_timeout = socket_timeout
            self.retry_on_timeout = retry_on_timeout
            self.health_check_interval = health_check_interval
            self.next_health_check = 0
            self.encoder = Encoder(encoding, encoding_errors, decode_responses)
            self._sock = None
            self._parser = parser_class(socket_read_size=socket_read_size)
            self._connect_callbacks = []
            self._buffer_cutoff = 6000

        def repr_pieces(self):
            pieces = [
             (
              'path', self.path),
             (
              'db', self.db)]
            if self.client_name:
                pieces.append(('client_name', self.client_name))
            return pieces

        def _connect(self):
            """Create a Unix domain socket connection"""
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(self.socket_timeout)
            sock.connect(self.path)
            return sock

        def _error_message(self, exception):
            if len(exception.args) == 1:
                return 'Error connecting to unix socket: %s. %s.' % (
                 self.path, exception.args[0])
            return 'Error %s connecting to unix socket: %s. %s.' % (
             exception.args[0], self.path, exception.args[1])


    FALSE_STRINGS = ('0', 'F', 'FALSE', 'N', 'NO')

    def to_bool(value):
        if value is None or value == '':
            return
        if isinstance(value, basestring):
            if value.upper() in FALSE_STRINGS:
                return False
        return bool(value)


    URL_QUERY_ARGUMENT_PARSERS = {'socket_timeout':float, 
     'socket_connect_timeout':float, 
     'socket_keepalive':to_bool, 
     'retry_on_timeout':to_bool, 
     'max_connections':int, 
     'health_check_interval':int, 
     'ssl_check_hostname':to_bool}

    class ConnectionPool(object):
        __doc__ = 'Generic connection pool'

        @classmethod
        def from_url(cls, url, db=None, decode_components=False, **kwargs):
            """
        Return a connection pool configured from the given URL.

        For example::

            redis://[[username]:[password]]@localhost:6379/0
            rediss://[[username]:[password]]@localhost:6379/0
            unix://[[username]:[password]]@/path/to/socket.sock?db=0

        Three URL schemes are supported:

        - ```redis://``
          <https://www.iana.org/assignments/uri-schemes/prov/redis>`_ creates a
          normal TCP socket connection
        - ```rediss://``
          <https://www.iana.org/assignments/uri-schemes/prov/rediss>`_ creates
          a SSL wrapped TCP socket connection
        - ``unix://`` creates a Unix Domain Socket connection

        There are several ways to specify a database number. The parse function
        will return the first specified option:
            1. A ``db`` querystring option, e.g. redis://localhost?db=0
            2. If using the redis:// scheme, the path argument of the url, e.g.
               redis://localhost/0
            3. The ``db`` argument to this function.

        If none of these options are specified, db=0 is used.

        The ``decode_components`` argument allows this function to work with
        percent-encoded URLs. If this argument is set to ``True`` all ``%xx``
        escapes will be replaced by their single-character equivalents after
        the URL has been parsed. This only applies to the ``hostname``,
        ``path``, ``username`` and ``password`` components.

        Any additional querystring arguments and keyword arguments will be
        passed along to the ConnectionPool class's initializer. The querystring
        arguments ``socket_connect_timeout`` and ``socket_timeout`` if supplied
        are parsed as float values. The arguments ``socket_keepalive`` and
        ``retry_on_timeout`` are parsed to boolean values that accept
        True/False, Yes/No values to indicate state. Invalid types cause a
        ``UserWarning`` to be raised. In the case of conflicting arguments,
        querystring arguments always win.

        """
            url = urlparse(url)
            url_options = {}
            for name, value in iteritems(parse_qs(url.query)):
                if value:
                    if len(value) > 0:
                        parser = URL_QUERY_ARGUMENT_PARSERS.get(name)
                        if parser:
                            try:
                                url_options[name] = parser(value[0])
                            except (TypeError, ValueError):
                                warnings.warn(UserWarning('Invalid value for `%s` in connection URL.' % name))

                        else:
                            url_options[name] = value[0]
                    if decode_components:
                        username = unquote(url.username) if url.username else None
                        password = unquote(url.password) if url.password else None
                        path = unquote(url.path) if url.path else None
                        hostname = unquote(url.hostname) if url.hostname else None
                    else:
                        username = url.username or None
                        password = url.password or None
                        path = url.path
                        hostname = url.hostname
                    if url.scheme == 'unix':
                        url_options.update({'username':username, 
                         'password':password, 
                         'path':path, 
                         'connection_class':UnixDomainSocketConnection})
                    else:
                        if url.scheme in ('redis', 'rediss'):
                            url_options.update({'host':hostname, 
                             'port':int(url.port or 6379), 
                             'username':username, 
                             'password':password})
                            if 'db' not in url_options:
                                if path:
                                    try:
                                        url_options['db'] = int(path.replace('/', ''))
                                    except (AttributeError, ValueError):
                                        pass

                            if url.scheme == 'rediss':
                                url_options['connection_class'] = SSLConnection
                        else:
                            valid_schemes = ', '.join(('redis://', 'rediss://', 'unix://'))
                            raise ValueError('Redis URL must specify one of the followingschemes (%s)' % valid_schemes)
                    url_options['db'] = int(url_options.get('db', db or 0))
                    kwargs.update(url_options)
                    if 'charset' in kwargs:
                        warnings.warn(DeprecationWarning('"charset" is deprecated. Use "encoding" instead'))
                        kwargs['encoding'] = kwargs.pop('charset')
                    if 'errors' in kwargs:
                        warnings.warn(DeprecationWarning('"errors" is deprecated. Use "encoding_errors" instead'))
                        kwargs['encoding_errors'] = kwargs.pop('errors')
                return cls(**kwargs)

        def __init__(self, connection_class=Connection, max_connections=None, **connection_kwargs):
            """
        Create a connection pool. If max_connections is set, then this
        object raises redis.ConnectionError when the pool's limit is reached.

        By default, TCP connections are created unless connection_class is
        specified. Use redis.UnixDomainSocketConnection for unix sockets.

        Any additional keyword arguments are passed to the constructor of
        connection_class.
        """
            max_connections = max_connections or 2147483648
            if not isinstance(max_connections, (int, long)) or max_connections < 0:
                raise ValueError('"max_connections" must be a positive integer')
            self.connection_class = connection_class
            self.connection_kwargs = connection_kwargs
            self.max_connections = max_connections
            self._fork_lock = threading.Lock()
            self.reset()

        def __repr__(self):
            return '%s<%s>' % (
             type(self).__name__,
             repr((self.connection_class)(**self.connection_kwargs)))

        def reset(self):
            self._lock = threading.RLock()
            self._created_connections = 0
            self._available_connections = []
            self._in_use_connections = set()
            self.pid = os.getpid()

        def _checkpid(self):
            if self.pid != os.getpid():
                timeout_at = time() + 5
                acquired = False
                while time() < timeout_at:
                    acquired = self._fork_lock.acquire(False)
                    if acquired:
                        break

                if not acquired:
                    raise ChildDeadlockedError
                try:
                    if self.pid != os.getpid():
                        self.reset()
                finally:
                    self._fork_lock.release()

        def get_connection--- This code section failed: ---

 L.1176         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _checkpid
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L.1177         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _lock
               12  SETUP_WITH          200  'to 200'
               14  POP_TOP          

 L.1178        16  SETUP_FINALLY        32  'to 32'

 L.1179        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _available_connections
               22  LOAD_METHOD              pop
               24  CALL_METHOD_0         0  ''
               26  STORE_FAST               'connection'
               28  POP_BLOCK        
               30  JUMP_FORWARD         60  'to 60'
             32_0  COME_FROM_FINALLY    16  '16'

 L.1180        32  DUP_TOP          
               34  LOAD_GLOBAL              IndexError
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    58  'to 58'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L.1181        46  LOAD_FAST                'self'
               48  LOAD_METHOD              make_connection
               50  CALL_METHOD_0         0  ''
               52  STORE_FAST               'connection'
               54  POP_EXCEPT       
               56  JUMP_FORWARD         60  'to 60'
             58_0  COME_FROM            38  '38'
               58  END_FINALLY      
             60_0  COME_FROM            56  '56'
             60_1  COME_FROM            30  '30'

 L.1182        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _in_use_connections
               64  LOAD_METHOD              add
               66  LOAD_FAST                'connection'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L.1183        72  SETUP_FINALLY       160  'to 160'

 L.1185        74  LOAD_FAST                'connection'
               76  LOAD_METHOD              connect
               78  CALL_METHOD_0         0  ''
               80  POP_TOP          

 L.1190        82  SETUP_FINALLY       104  'to 104'

 L.1191        84  LOAD_FAST                'connection'
               86  LOAD_METHOD              can_read
               88  CALL_METHOD_0         0  ''
               90  POP_JUMP_IF_FALSE   100  'to 100'

 L.1192        92  LOAD_GLOBAL              ConnectionError
               94  LOAD_STR                 'Connection has data'
               96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  'exception instance'
            100_0  COME_FROM            90  '90'
              100  POP_BLOCK        
              102  JUMP_FORWARD        156  'to 156'
            104_0  COME_FROM_FINALLY    82  '82'

 L.1193       104  DUP_TOP          
              106  LOAD_GLOBAL              ConnectionError
              108  COMPARE_OP               exception-match
              110  POP_JUMP_IF_FALSE   154  'to 154'
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L.1194       118  LOAD_FAST                'connection'
              120  LOAD_METHOD              disconnect
              122  CALL_METHOD_0         0  ''
              124  POP_TOP          

 L.1195       126  LOAD_FAST                'connection'
              128  LOAD_METHOD              connect
              130  CALL_METHOD_0         0  ''
              132  POP_TOP          

 L.1196       134  LOAD_FAST                'connection'
              136  LOAD_METHOD              can_read
              138  CALL_METHOD_0         0  ''
              140  POP_JUMP_IF_FALSE   150  'to 150'

 L.1197       142  LOAD_GLOBAL              ConnectionError
              144  LOAD_STR                 'Connection not ready'
              146  CALL_FUNCTION_1       1  ''
              148  RAISE_VARARGS_1       1  'exception instance'
            150_0  COME_FROM           140  '140'
              150  POP_EXCEPT       
              152  JUMP_FORWARD        156  'to 156'
            154_0  COME_FROM           110  '110'
              154  END_FINALLY      
            156_0  COME_FROM           152  '152'
            156_1  COME_FROM           102  '102'
              156  POP_BLOCK        
              158  JUMP_FORWARD        184  'to 184'
            160_0  COME_FROM_FINALLY    72  '72'

 L.1198       160  POP_TOP          
              162  POP_TOP          
              164  POP_TOP          

 L.1201       166  LOAD_FAST                'self'
              168  LOAD_METHOD              release
              170  LOAD_FAST                'connection'
              172  CALL_METHOD_1         1  ''
              174  POP_TOP          

 L.1202       176  RAISE_VARARGS_0       0  'reraise'
              178  POP_EXCEPT       
              180  JUMP_FORWARD        184  'to 184'
              182  END_FINALLY      
            184_0  COME_FROM           180  '180'
            184_1  COME_FROM           158  '158'

 L.1204       184  LOAD_FAST                'connection'
              186  POP_BLOCK        
              188  ROT_TWO          
              190  BEGIN_FINALLY    
              192  WITH_CLEANUP_START
              194  WITH_CLEANUP_FINISH
              196  POP_FINALLY           0  ''
              198  RETURN_VALUE     
            200_0  COME_FROM_WITH       12  '12'
              200  WITH_CLEANUP_START
              202  WITH_CLEANUP_FINISH
              204  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 188

        def get_encoder(self):
            """Return an encoder based on encoding settings"""
            kwargs = self.connection_kwargs
            return Encoder(encoding=(kwargs.get('encoding', 'utf-8')),
              encoding_errors=(kwargs.get('encoding_errors', 'strict')),
              decode_responses=(kwargs.get('decode_responses', False)))

        def make_connection(self):
            """Create a new connection"""
            if self._created_connections >= self.max_connections:
                raise ConnectionError('Too many connections')
            self._created_connections += 1
            return (self.connection_class)(**self.connection_kwargs)

        def release--- This code section failed: ---

 L.1224         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _checkpid
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L.1225         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _lock
               12  SETUP_WITH           70  'to 70'
               14  POP_TOP          

 L.1226        16  LOAD_FAST                'connection'
               18  LOAD_ATTR                pid
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                pid
               24  COMPARE_OP               !=
               26  POP_JUMP_IF_FALSE    42  'to 42'

 L.1227        28  POP_BLOCK        
               30  BEGIN_FINALLY    
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  POP_FINALLY           0  ''
               38  LOAD_CONST               None
               40  RETURN_VALUE     
             42_0  COME_FROM            26  '26'

 L.1228        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _in_use_connections
               46  LOAD_METHOD              remove
               48  LOAD_FAST                'connection'
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L.1229        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _available_connections
               58  LOAD_METHOD              append
               60  LOAD_FAST                'connection'
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          
               66  POP_BLOCK        
               68  BEGIN_FINALLY    
             70_0  COME_FROM_WITH       12  '12'
               70  WITH_CLEANUP_START
               72  WITH_CLEANUP_FINISH
               74  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 30

        def disconnect(self):
            """Disconnects all connections in the pool"""
            self._checkpid()
            with self._lock:
                all_conns = chain(self._available_connections, self._in_use_connections)
                for connection in all_conns:
                    connection.disconnect()


    class BlockingConnectionPool(ConnectionPool):
        __doc__ = '\n    Thread-safe blocking connection pool::\n\n        >>> from redis.client import Redis\n        >>> client = Redis(connection_pool=BlockingConnectionPool())\n\n    It performs the same function as the default\n    ``:py:class: ~redis.connection.ConnectionPool`` implementation, in that,\n    it maintains a pool of reusable connections that can be shared by\n    multiple redis clients (safely across threads if required).\n\n    The difference is that, in the event that a client tries to get a\n    connection from the pool when all of connections are in use, rather than\n    raising a ``:py:class: ~redis.exceptions.ConnectionError`` (as the default\n    ``:py:class: ~redis.connection.ConnectionPool`` implementation does), it\n    makes the client wait ("blocks") for a specified number of seconds until\n    a connection becomes available.\n\n    Use ``max_connections`` to increase / decrease the pool size::\n\n        >>> pool = BlockingConnectionPool(max_connections=10)\n\n    Use ``timeout`` to tell it either how many seconds to wait for a connection\n    to become available, or to block forever:\n\n        # Block forever.\n        >>> pool = BlockingConnectionPool(timeout=None)\n\n        # Raise a ``ConnectionError`` after five seconds if a connection is\n        # not available.\n        >>> pool = BlockingConnectionPool(timeout=5)\n    '

        def __init__(self, max_connections=50, timeout=20, connection_class=Connection, queue_class=LifoQueue, **connection_kwargs):
            self.queue_class = queue_class
            self.timeout = timeout
            (super(BlockingConnectionPool, self).__init__)(connection_class=connection_class, 
             max_connections=max_connections, **connection_kwargs)

        def reset(self):
            self.pool = self.queue_class(self.max_connections)
            while True:
                try:
                    self.pool.put_nowait(None)
                except Full:
                    break

            self._connections = []
            self.pid = os.getpid()

        def make_connection(self):
            """Make a fresh connection."""
            connection = (self.connection_class)(**self.connection_kwargs)
            self._connections.append(connection)
            return connection

        def get_connection(self, command_name, *keys, **options):
            """
        Get a connection, blocking for ``self.timeout`` until a connection
        is available from the pool.

        If the connection returned is ``None`` then creates a new connection.
        Because we use a last-in first-out queue, the existing connections
        (having been returned to the pool after the initial ``None`` values
        were added) will be returned before ``None`` values. This means we only
        create new connections when we need to, i.e.: the actual number of
        connections will only increase in response to demand.
        """
            self._checkpid()
            connection = None
            try:
                connection = self.pool.get(block=True, timeout=(self.timeout))
            except Empty:
                raise ConnectionError('No connection available.')
            else:
                if connection is None:
                    connection = self.make_connection()
                try:
                    connection.connect()
                    try:
                        if connection.can_read():
                            raise ConnectionError('Connection has data')
                    except ConnectionError:
                        connection.disconnect()
                        connection.connect()
                        if connection.can_read():
                            raise ConnectionError('Connection not ready')

                except:
                    self.release(connection)
                    raise
                else:
                    return connection

        def release(self, connection):
            """Releases the connection back to the pool."""
            self._checkpid()
            if connection.pid != self.pid:
                return
            try:
                self.pool.put_nowait(connection)
            except Full:
                pass

        def disconnect(self):
            """Disconnects all connections in the pool."""
            self._checkpid()
            for connection in self._connections:
                connection.disconnect()