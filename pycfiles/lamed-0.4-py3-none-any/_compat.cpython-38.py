# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-03p63p8r/redis/redis/_compat.py
# Compiled at: 2020-04-05 04:25:10
# Size of source mod 2**32: 5649 bytes
"""Internal module for Python 2 backwards compatibility."""
import errno, socket, sys

def sendall(sock, *args, **kwargs):
    return (sock.sendall)(*args, **kwargs)


def shutdown(sock, *args, **kwargs):
    return (sock.shutdown)(*args, **kwargs)


def ssl_wrap_socket(context, sock, *args, **kwargs):
    return (context.wrap_socket)(sock, *args, **kwargs)


if not (sys.version_info[0] < 3 or sys.version_info[0]) == 3 or sys.version_info[1] < 5:
    import time

    def _retryable_call--- This code section failed: ---

 L.  30         0  LOAD_CONST               (None, 0.0)
                2  UNPACK_SEQUENCE_2     2 
                4  STORE_FAST               'timeout'
                6  STORE_FAST               'deadline'

 L.  31         8  LOAD_CONST               False
               10  STORE_FAST               'attempted'

 L.  32        12  SETUP_FINALLY        26  'to 26'

 L.  33        14  LOAD_FAST                's'
               16  LOAD_METHOD              gettimeout
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               'timeout'
               22  POP_BLOCK        
               24  JUMP_FORWARD         46  'to 46'
             26_0  COME_FROM_FINALLY    12  '12'

 L.  34        26  DUP_TOP          
               28  LOAD_GLOBAL              AttributeError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    44  'to 44'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.  35        40  POP_EXCEPT       
               42  JUMP_FORWARD         46  'to 46'
             44_0  COME_FROM            32  '32'
               44  END_FINALLY      
             46_0  COME_FROM            42  '42'
             46_1  COME_FROM            24  '24'

 L.  37        46  LOAD_FAST                'timeout'
               48  POP_JUMP_IF_FALSE    62  'to 62'

 L.  38        50  LOAD_GLOBAL              time
               52  LOAD_METHOD              time
               54  CALL_METHOD_0         0  ''
               56  LOAD_FAST                'timeout'
               58  BINARY_ADD       
               60  STORE_FAST               'deadline'
             62_0  COME_FROM            48  '48'

 L.  40        62  SETUP_FINALLY       208  'to 208'

 L.  42        64  LOAD_FAST                'attempted'
               66  POP_JUMP_IF_FALSE   118  'to 118'
               68  LOAD_FAST                'timeout'
               70  POP_JUMP_IF_FALSE   118  'to 118'

 L.  43        72  LOAD_GLOBAL              time
               74  LOAD_METHOD              time
               76  CALL_METHOD_0         0  ''
               78  STORE_FAST               'now'

 L.  44        80  LOAD_FAST                'now'
               82  LOAD_FAST                'deadline'
               84  COMPARE_OP               >=
               86  POP_JUMP_IF_FALSE   104  'to 104'

 L.  45        88  LOAD_GLOBAL              socket
               90  LOAD_METHOD              error
               92  LOAD_GLOBAL              errno
               94  LOAD_ATTR                EWOULDBLOCK
               96  LOAD_STR                 'timed out'
               98  CALL_METHOD_2         2  ''
              100  RAISE_VARARGS_1       1  'exception instance'
              102  JUMP_FORWARD        118  'to 118'
            104_0  COME_FROM            86  '86'

 L.  49       104  LOAD_FAST                's'
              106  LOAD_METHOD              settimeout
              108  LOAD_FAST                'deadline'
              110  LOAD_FAST                'now'
              112  BINARY_SUBTRACT  
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          
            118_0  COME_FROM           102  '102'
            118_1  COME_FROM            70  '70'
            118_2  COME_FROM            66  '66'

 L.  50       118  SETUP_FINALLY       140  'to 140'

 L.  51       120  LOAD_CONST               True
              122  STORE_FAST               'attempted'

 L.  52       124  LOAD_FAST                'func'
              126  LOAD_FAST                'args'
              128  LOAD_FAST                'kwargs'
              130  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              132  POP_BLOCK        
              134  POP_BLOCK        
              136  CALL_FINALLY        208  'to 208'
              138  RETURN_VALUE     
            140_0  COME_FROM_FINALLY   118  '118'

 L.  53       140  DUP_TOP          
              142  LOAD_GLOBAL              socket
              144  LOAD_ATTR                error
              146  COMPARE_OP               exception-match
              148  POP_JUMP_IF_FALSE   200  'to 200'
              150  POP_TOP          
              152  STORE_FAST               'e'
              154  POP_TOP          
              156  SETUP_FINALLY       188  'to 188'

 L.  54       158  LOAD_FAST                'e'
              160  LOAD_ATTR                args
              162  LOAD_CONST               0
              164  BINARY_SUBSCR    
              166  LOAD_GLOBAL              errno
              168  LOAD_ATTR                EINTR
              170  COMPARE_OP               ==
              172  POP_JUMP_IF_FALSE   182  'to 182'

 L.  55       174  POP_BLOCK        
              176  POP_EXCEPT       
              178  CALL_FINALLY        188  'to 188'
              180  JUMP_BACK            64  'to 64'
            182_0  COME_FROM           172  '172'

 L.  56       182  RAISE_VARARGS_0       0  'reraise'
              184  POP_BLOCK        
              186  BEGIN_FINALLY    
            188_0  COME_FROM           178  '178'
            188_1  COME_FROM_FINALLY   156  '156'
              188  LOAD_CONST               None
              190  STORE_FAST               'e'
              192  DELETE_FAST              'e'
              194  END_FINALLY      
              196  POP_EXCEPT       
              198  JUMP_BACK            64  'to 64'
            200_0  COME_FROM           148  '148'
              200  END_FINALLY      
              202  JUMP_BACK            64  'to 64'
              204  POP_BLOCK        
              206  BEGIN_FINALLY    
            208_0  COME_FROM           136  '136'
            208_1  COME_FROM_FINALLY    62  '62'

 L.  60       208  LOAD_FAST                'timeout'
              210  POP_JUMP_IF_FALSE   222  'to 222'

 L.  61       212  LOAD_FAST                's'
              214  LOAD_METHOD              settimeout
              216  LOAD_FAST                'timeout'
              218  CALL_METHOD_1         1  ''
              220  POP_TOP          
            222_0  COME_FROM           210  '210'
              222  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 134


    def recv(sock, *args, **kwargs):
        return _retryable_call(sock, sock.recv, *args, **kwargs)


    def recv_into(sock, *args, **kwargs):
        return _retryable_call(sock, sock.recv_into, *args, **kwargs)


else:

    def recv(sock, *args, **kwargs):
        return (sock.recv)(*args, **kwargs)


    def recv_into(sock, *args, **kwargs):
        return (sock.recv_into)(*args, **kwargs)


if sys.version_info[0] < 3:
    import functools
    try:
        from ssl import SSLError as _SSLError
    except ImportError:

        class _SSLError(Exception):
            __doc__ = 'A replacement in case ssl.SSLError is not available.'


    else:
        _EXPECTED_SSL_TIMEOUT_MESSAGES = ('The handshake operation timed out', 'The read operation timed out',
                                          'The write operation timed out')

        def _handle_ssl_timeout(func):

            @functools.wrapsfunc
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                            except _SSLError as e:
                    try:
                        message = len(e.args) == 1 and unicode(e.args[0]) or ''
                        if any((x in message for x in _EXPECTED_SSL_TIMEOUT_MESSAGES)):
                            raise (socket.timeout)(*e.args)
                        raise
                    finally:
                        e = None
                        del e

            return wrapper


        recv = _handle_ssl_timeout(recv)
        recv_into = _handle_ssl_timeout(recv_into)
        sendall = _handle_ssl_timeout(sendall)
        shutdown = _handle_ssl_timeout(shutdown)
        ssl_wrap_socket = _handle_ssl_timeout(ssl_wrap_socket)
elif sys.version_info[0] < 3:
    from urllib import unquote
    from urlparse import parse_qs, urlparse
    from itertools import imap, izip
    from string import letters as ascii_letters
    from Queue import Queue

    def safe_unicode--- This code section failed: ---

 L. 124         0  SETUP_FINALLY        18  'to 18'

 L. 125         2  LOAD_GLOBAL              unicode
                4  LOAD_FAST                'obj'
                6  BUILD_TUPLE_1         1 
                8  LOAD_FAST                'args'
               10  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
               12  CALL_FUNCTION_EX      0  'positional arguments only'
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L. 126        18  DUP_TOP          
               20  LOAD_GLOBAL              UnicodeDecodeError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    58  'to 58'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 128        32  LOAD_GLOBAL              str
               34  LOAD_FAST                'obj'
               36  CALL_FUNCTION_1       1  ''
               38  LOAD_METHOD              encode
               40  LOAD_STR                 'string_escape'
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'ascii_text'

 L. 129        46  LOAD_GLOBAL              unicode
               48  LOAD_FAST                'ascii_text'
               50  CALL_FUNCTION_1       1  ''
               52  ROT_FOUR         
               54  POP_EXCEPT       
               56  RETURN_VALUE     
             58_0  COME_FROM            24  '24'
               58  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 28


    def iteritems(x):
        return x.iteritems


    def iterkeys(x):
        return x.iterkeys


    def itervalues(x):
        return x.itervalues


    def nativestr(x):
        if isinstance(x, str):
            return x
        return x.encode'utf-8''replace'


    def next(x):
        return x.next


    def byte_to_chr(x):
        return x


    unichr = unichr
    xrange = xrange
    basestring = basestring
    unicode = unicode
    long = long
    BlockingIOError = socket.error
else:
    from urllib.parse import parse_qs, unquote, urlparse
    from string import ascii_letters
    from queue import Queue

    def iteritems(x):
        return iter(x.items)


    def iterkeys(x):
        return iter(x.keys)


    def itervalues(x):
        return iter(x.values)


    def byte_to_chr(x):
        return chr(x)


    def nativestr(x):
        if isinstance(x, str):
            return x
        return x.decode'utf-8''replace'


    next = next
    unichr = chr
    imap = map
    izip = zip
    xrange = range
    basestring = str
    unicode = str
    safe_unicode = str
    long = int
    BlockingIOError = BlockingIOError
try:
    from queue import LifoQueue, Empty, Full
except ImportError:
    from Queue import LifoQueue, Empty, Full