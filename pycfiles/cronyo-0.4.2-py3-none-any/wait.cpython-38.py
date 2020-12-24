# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./vendor/urllib3/util/wait.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 5406 bytes
import errno
from functools import partial
import select, sys
try:
    from time import monotonic
except ImportError:
    from time import time as monotonic
else:
    __all__ = [
     'NoWayToWaitForSocketError', 'wait_for_read', 'wait_for_write']

    class NoWayToWaitForSocketError(Exception):
        pass


    if sys.version_info >= (3, 5):

        def _retry_on_intr(fn, timeout):
            return fn(timeout)


    else:

        def _retry_on_intr--- This code section failed: ---

 L.  49         0  LOAD_FAST                'timeout'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L.  50         8  LOAD_GLOBAL              float
               10  LOAD_STR                 'inf'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'deadline'
               16  JUMP_FORWARD         28  'to 28'
             18_0  COME_FROM             6  '6'

 L.  52        18  LOAD_GLOBAL              monotonic
               20  CALL_FUNCTION_0       0  ''
               22  LOAD_FAST                'timeout'
               24  BINARY_ADD       
               26  STORE_FAST               'deadline'
             28_0  COME_FROM            16  '16'

 L.  55        28  SETUP_FINALLY        40  'to 40'

 L.  56        30  LOAD_FAST                'fn'
               32  LOAD_FAST                'timeout'
               34  CALL_FUNCTION_1       1  ''
               36  POP_BLOCK        
               38  RETURN_VALUE     
             40_0  COME_FROM_FINALLY    28  '28'

 L.  58        40  DUP_TOP          
               42  LOAD_GLOBAL              OSError
               44  LOAD_GLOBAL              select
               46  LOAD_ATTR                error
               48  BUILD_TUPLE_2         2 
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE   144  'to 144'
               54  POP_TOP          
               56  STORE_FAST               'e'
               58  POP_TOP          
               60  SETUP_FINALLY       132  'to 132'

 L.  60        62  LOAD_FAST                'e'
               64  LOAD_ATTR                args
               66  LOAD_CONST               0
               68  BINARY_SUBSCR    
               70  LOAD_GLOBAL              errno
               72  LOAD_ATTR                EINTR
               74  COMPARE_OP               !=
               76  POP_JUMP_IF_FALSE    82  'to 82'

 L.  61        78  RAISE_VARARGS_0       0  'reraise'
               80  JUMP_FORWARD        128  'to 128'
             82_0  COME_FROM            76  '76'

 L.  63        82  LOAD_FAST                'deadline'
               84  LOAD_GLOBAL              monotonic
               86  CALL_FUNCTION_0       0  ''
               88  BINARY_SUBTRACT  
               90  STORE_FAST               'timeout'

 L.  64        92  LOAD_FAST                'timeout'
               94  LOAD_CONST               0
               96  COMPARE_OP               <
               98  POP_JUMP_IF_FALSE   104  'to 104'

 L.  65       100  LOAD_CONST               0
              102  STORE_FAST               'timeout'
            104_0  COME_FROM            98  '98'

 L.  66       104  LOAD_FAST                'timeout'
              106  LOAD_GLOBAL              float
              108  LOAD_STR                 'inf'
              110  CALL_FUNCTION_1       1  ''
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   120  'to 120'

 L.  67       116  LOAD_CONST               None
              118  STORE_FAST               'timeout'
            120_0  COME_FROM           114  '114'

 L.  68       120  POP_BLOCK        
              122  POP_EXCEPT       
              124  CALL_FINALLY        132  'to 132'
              126  JUMP_BACK            28  'to 28'
            128_0  COME_FROM            80  '80'
              128  POP_BLOCK        
              130  BEGIN_FINALLY    
            132_0  COME_FROM           124  '124'
            132_1  COME_FROM_FINALLY    60  '60'
              132  LOAD_CONST               None
              134  STORE_FAST               'e'
              136  DELETE_FAST              'e'
              138  END_FINALLY      
              140  POP_EXCEPT       
              142  JUMP_BACK            28  'to 28'
            144_0  COME_FROM            52  '52'
              144  END_FINALLY      
              146  JUMP_BACK            28  'to 28'

Parse error at or near `POP_EXCEPT' instruction at offset 122


    def select_wait_for_socket(sock, read=False, write=False, timeout=None):
        if not read:
            if not write:
                raise RuntimeError('must specify at least one of read=True, write=True')
        rcheck = []
        wcheck = []
        if read:
            rcheck.append(sock)
        if write:
            wcheck.append(sock)
        fn = partial(select.select, rcheck, wcheck, wcheck)
        rready, wready, xready = _retry_on_intr(fn, timeout)
        return bool(rready or wready or xready)


    def poll_wait_for_socket(sock, read=False, write=False, timeout=None):
        if not read:
            if not write:
                raise RuntimeError('must specify at least one of read=True, write=True')
        mask = 0
        if read:
            mask |= select.POLLIN
        if write:
            mask |= select.POLLOUT
        poll_obj = select.poll()
        poll_obj.register(sock, mask)

        def do_poll(t):
            if t is not None:
                t *= 1000
            return poll_obj.poll(t)

        return bool(_retry_on_intr(do_poll, timeout))


    def null_wait_for_socket(*args, **kwargs):
        raise NoWayToWaitForSocketError('no select-equivalent available')


    def _have_working_poll():
        try:
            poll_obj = select.poll()
            _retry_on_intr(poll_obj.poll, 0)
        except (AttributeError, OSError):
            return False
        else:
            return True


    def wait_for_socket(*args, **kwargs):
        global wait_for_socket
        if _have_working_poll:
            wait_for_socket = poll_wait_for_socket
        else:
            if hasattr(select, 'select'):
                wait_for_socket = select_wait_for_socket
            else:
                wait_for_socket = null_wait_for_socket
        return wait_for_socket(*args, **kwargs)


    def wait_for_read(sock, timeout=None):
        """ Waits for reading to be available on a given socket.
    Returns True if the socket is readable, or False if the timeout expired.
    """
        return wait_for_socket(sock, read=True, timeout=timeout)


    def wait_for_write(sock, timeout=None):
        """ Waits for writing to be available on a given socket.
    Returns True if the socket is readable, or False if the timeout expired.
    """
        return wait_for_socket(sock, write=True, timeout=timeout)