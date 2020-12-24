# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/archipelagentvirtualmachinestorage/magic.py
# Compiled at: 2013-03-20 13:50:16
__doc__ = '\nmagic is a wrapper around the libmagic file identification library.\n\nSee README for more information.\n\nUsage:\n\n>>> import magic\n>>> magic.from_file("testdata/test.pdf")\n\'PDF document, version 1.2\'\n>>> magic.from_file("testdata/test.pdf", mime=True)\n\'application/pdf\'\n>>> magic.from_buffer(open("testdata/test.pdf").read(1024))\n\'PDF document, version 1.2\'\n>>>\n\n\n'
import os.path, ctypes, ctypes.util
from ctypes import c_char_p, c_int, c_size_t, c_void_p

class MagicException(Exception):
    pass


class Magic:
    """
    Magic is a wrapper around the libmagic C library.

    """

    def __init__(self, mime=False, magic_file=None, mime_encoding=False):
        """
        Create a new libmagic wrapper.

        mime - if True, mimetypes are returned instead of textual descriptions
        mime_encoding - if True, codec is returned
        magic_file - use a mime database other than the system default

        """
        flags = MAGIC_NONE
        if mime:
            flags |= MAGIC_MIME
        elif mime_encoding:
            flags |= MAGIC_MIME_ENCODING
        self.cookie = magic_open(flags)
        magic_load(self.cookie, magic_file)

    def from_buffer(self, buf):
        """
        Identify the contents of `buf`
        """
        return magic_buffer(self.cookie, buf)

    def from_file(self, filename):
        """
        Identify the contents of file `filename`
        raises IOError if the file does not exist
        """
        if not os.path.exists(filename):
            raise IOError('File does not exist: ' + filename)
        return magic_file(self.cookie, filename)

    def __del__(self):
        if self.cookie:
            magic_close(self.cookie)
            self.cookie = None
        return


_magic_mime = None
_magic = None

def _get_magic_mime():
    global _magic_mime
    if not _magic_mime:
        _magic_mime = Magic(mime=True)
    return _magic_mime


def _get_magic():
    global _magic
    if not _magic:
        _magic = Magic()
    return _magic


def _get_magic_type(mime):
    if mime:
        return _get_magic_mime()
    else:
        return _get_magic()


def from_file(filename, mime=False):
    m = _get_magic_type(mime)
    return m.from_file(filename)


def from_buffer(buffer, mime=False):
    m = _get_magic_type(mime)
    return m.from_buffer(buffer)


libmagic = None
dll = ctypes.util.find_library('magic') or ctypes.util.find_library('magic1')
if dll:
    libmagic = ctypes.CDLL(dll)
if not libmagic or not libmagic._name:
    import sys
    platform_to_lib = {'darwin': '/opt/local/lib/libmagic.dylib', 'win32': 'magic1.dll'}
    if sys.platform in platform_to_lib:
        try:
            libmagic = ctypes.CDLL(platform_to_lib[sys.platform])
        except OSError:
            pass

if not libmagic or not libmagic._name:
    raise ImportError('failed to find libmagic.  Check your installation')
magic_t = ctypes.c_void_p

def errorcheck(result, func, args):
    err = magic_error(args[0])
    if err is not None:
        raise MagicException(err)
    else:
        return result
    return


magic_open = libmagic.magic_open
magic_open.restype = magic_t
magic_open.argtypes = [c_int]
magic_close = libmagic.magic_close
magic_close.restype = None
magic_close.argtypes = [magic_t]
magic_error = libmagic.magic_error
magic_error.restype = c_char_p
magic_error.argtypes = [magic_t]
magic_errno = libmagic.magic_errno
magic_errno.restype = c_int
magic_errno.argtypes = [magic_t]
magic_file = libmagic.magic_file
magic_file.restype = c_char_p
magic_file.argtypes = [magic_t, c_char_p]
magic_file.errcheck = errorcheck
_magic_buffer = libmagic.magic_buffer
_magic_buffer.restype = c_char_p
_magic_buffer.argtypes = [magic_t, c_void_p, c_size_t]
_magic_buffer.errcheck = errorcheck

def magic_buffer(cookie, buf):
    return _magic_buffer(cookie, buf, len(buf))


magic_load = libmagic.magic_load
magic_load.restype = c_int
magic_load.argtypes = [magic_t, c_char_p]
magic_load.errcheck = errorcheck
magic_setflags = libmagic.magic_setflags
magic_setflags.restype = c_int
magic_setflags.argtypes = [magic_t, c_int]
magic_check = libmagic.magic_check
magic_check.restype = c_int
magic_check.argtypes = [magic_t, c_char_p]
magic_compile = libmagic.magic_compile
magic_compile.restype = c_int
magic_compile.argtypes = [magic_t, c_char_p]
MAGIC_NONE = 0
MAGIC_DEBUG = 1
MAGIC_SYMLINK = 2
MAGIC_COMPRESS = 4
MAGIC_DEVICES = 8
MAGIC_MIME = 16
MAGIC_MIME_ENCODING = 1024
MAGIC_CONTINUE = 32
MAGIC_CHECK = 64
MAGIC_PRESERVE_ATIME = 128
MAGIC_RAW = 256
MAGIC_ERROR = 512
MAGIC_NO_CHECK_COMPRESS = 4096
MAGIC_NO_CHECK_TAR = 8192
MAGIC_NO_CHECK_SOFT = 16384
MAGIC_NO_CHECK_APPTYPE = 32768
MAGIC_NO_CHECK_ELF = 65536
MAGIC_NO_CHECK_ASCII = 131072
MAGIC_NO_CHECK_TROFF = 262144
MAGIC_NO_CHECK_FORTRAN = 524288
MAGIC_NO_CHECK_TOKENS = 1048576