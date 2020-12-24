# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/gunicorn/gunicorn/http/_sendfile.py
# Compiled at: 2019-02-14 00:35:18
import errno, os, sys
try:
    import ctypes, ctypes.util
except MemoryError:
    raise ImportError

SUPPORTED_PLATFORMS = ('darwin', 'freebsd', 'dragonfly', 'linux2')
if sys.platform not in SUPPORTED_PLATFORMS:
    raise ImportError("sendfile isn't supported on this platform")
_libc = ctypes.CDLL(ctypes.util.find_library('c'), use_errno=True)
_sendfile = _libc.sendfile

def sendfile(fdout, fdin, offset, nbytes):
    if sys.platform == 'darwin':
        _sendfile.argtypes = [
         ctypes.c_int, ctypes.c_int, ctypes.c_uint64,
         ctypes.POINTER(ctypes.c_uint64), ctypes.c_voidp,
         ctypes.c_int]
        _nbytes = ctypes.c_uint64(nbytes)
        result = _sendfile(fdin, fdout, offset, _nbytes, None, 0)
        if result == -1:
            e = ctypes.get_errno()
            if e == errno.EAGAIN and _nbytes.value is not None:
                return _nbytes.value
            raise OSError(e, os.strerror(e))
        return _nbytes.value
    else:
        if sys.platform in ('freebsd', 'dragonfly'):
            _sendfile.argtypes = [
             ctypes.c_int, ctypes.c_int, ctypes.c_uint64,
             ctypes.c_uint64, ctypes.c_voidp,
             ctypes.POINTER(ctypes.c_uint64), ctypes.c_int]
            _sbytes = ctypes.c_uint64()
            result = _sendfile(fdin, fdout, offset, nbytes, None, _sbytes, 0)
            if result == -1:
                e = ctypes.get_errno()
                if e == errno.EAGAIN and _sbytes.value is not None:
                    return _sbytes.value
                raise OSError(e, os.strerror(e))
            return _sbytes.value
        else:
            _sendfile.argtypes = [
             ctypes.c_int, ctypes.c_int,
             ctypes.POINTER(ctypes.c_uint64), ctypes.c_size_t]
            _offset = ctypes.c_uint64(offset)
            sent = _sendfile(fdout, fdin, _offset, nbytes)
            if sent == -1:
                e = ctypes.get_errno()
                raise OSError(e, os.strerror(e))
            return sent

        return