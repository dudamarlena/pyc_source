# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\cocos2020\cocos\audio\SDL\rwops.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 5337 bytes
"""General interface for SDL to read and write data sources.

For files, use `SDL_RWFromFile`.  Other Python file-type objects can be
used with `SDL_RWFromObject`.  If another library provides a constant void
pointer to a contiguous region of memory, `SDL_RWFromMem` and
`SDL_RWFromConstMem` can be used.
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: $'
from ctypes import *
from . import dll
from . import constants
_rwops_p = POINTER('SDL_RWops')
_seek_fn = CFUNCTYPE(c_int, _rwops_p, c_int, c_int)
_read_fn = CFUNCTYPE(c_int, _rwops_p, c_void_p, c_int, c_int)
_write_fn = CFUNCTYPE(c_int, _rwops_p, c_void_p, c_int, c_int)
_close_fn = CFUNCTYPE(c_int, _rwops_p)

class _hidden_mem_t(Structure):
    _fields_ = [
     (
      'base', c_void_p),
     (
      'here', c_void_p),
     (
      'stop', c_void_p)]


class SDL_RWops(Structure):
    __doc__ = 'Read/write operations structure.\n\n    :Ivariables:\n        `seek` : function\n            seek(context: `SDL_RWops`, offset: int, whence: int) -> int\n        `read` : function\n            read(context: `SDL_RWops`, ptr: c_void_p, size: int, maxnum: int)\n            -> int\n        `write` : function\n            write(context: `SDL_RWops`, ptr: c_void_p, size: int, num: int) ->\n            int\n        `close` : function\n            close(context: `SDL_RWops`) -> int\n        `type` : int\n            Undocumented\n\n    '
    _fields_ = [('seek', _seek_fn),
     (
      'read', _read_fn),
     (
      'write', _write_fn),
     (
      'close', _close_fn),
     (
      'type', c_uint),
     (
      '_hidden_mem', _hidden_mem_t)]


SetPointerType(_rwops_p, SDL_RWops)
SDL_RWFromFile = dll.function('SDL_RWFromFile',
  'Create an SDL_RWops structure from a file on disk.\n\n    :Parameters:\n        `file` : string\n            Filename\n        `mode` : string\n            Mode to open the file with; as with the built-in function ``open``.\n\n    :rtype: `SDL_RWops`\n    ',
  args=[
 'file', 'mode'],
  arg_types=[
 c_char_p, c_char_p],
  return_type=(POINTER(SDL_RWops)),
  dereference_return=True,
  require_return=True)
SDL_RWFromMem = dll.function('SDL_RWFromMem',
  'Create an SDL_RWops structure from a contiguous region of memory.\n\n    :Parameters:\n     - `mem`: ``c_void_p``\n     - `size`: int\n\n    :rtype: `SDL_RWops`\n    ',
  args=[
 'mem', 'size'],
  arg_types=[
 c_void_p, c_int],
  return_type=(POINTER(SDL_RWops)),
  dereference_return=True,
  require_return=True)
SDL_RWFromConstMem = dll.function('SDL_RWFromConstMem',
  'Create an SDL_RWops structure from a contiguous region of memory.\n\n    :Parameters:\n        `mem`: ``c_void_p``\n        `size`: int\n\n    :rtype: `SDL_RWops`\n    :since: 1.2.7\n    ',
  args=[
 'mem', 'size'],
  arg_types=[
 c_void_p, c_int],
  return_type=(POINTER(SDL_RWops)),
  dereference_return=True,
  require_return=True,
  since=(1, 2, 7))

def SDL_RWFromObject(obj):
    """Construct an SDL_RWops structure from a Python file-like object.

    The object must support the following methods in the same fashion as
    the builtin file object:

        - ``read(len) -> data``
        - ``write(data)``
        - ``seek(offset, whence)``
        - ``close()``

    :Parameters:
     - `obj`: Python file-like object to wrap

    :rtype: `SDL_RWops`
    """
    ctx = SDL_RWops()

    def _seek(context, offset, whence):
        obj.seek(offset, whence)
        return obj.tell()

    ctx.seek = _seek_fn(_seek)

    def _read(context, ptr, size, maximum):
        try:
            r = obj.read(maximum * size)
            memmove(ptr, r, len(r))
            return len(r) / size
        except:
            return -1

    ctx.read = _read_fn(_read)

    def _write(context, ptr, size, num):
        try:
            obj.write(string_at(ptr, size * num))
            return num
        except:
            return -1

    ctx.write = _write_fn(_write)

    def _close(context):
        obj.close()

    ctx.close = _close_fn(_close)
    return ctx