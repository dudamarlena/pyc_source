# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: d:\dev\cocos2020\cocos\audio\SDL\version.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 2165 bytes
__doc__ = 'Functions related to the SDL shared library version.\n'
__docformat__ = 'restructuredtext'
__version__ = '$Id: $'
from ctypes import *
from . import dll

class SDL_version(Structure):
    """SDL_version"""
    _fields_ = [
     (
      'major', c_ubyte),
     (
      'minor', c_ubyte),
     (
      'patch', c_ubyte)]

    def __repr__(self):
        return '%d.%d.%d' % (
         self.major, self.minor, self.patch)

    def is_since(self, required):
        if hasattr(required, 'major'):
            return self.major >= required.major and self.minor >= required.minor and self.patch >= required.patch
        return self.major >= required[0] and self.minor >= required[1] and self.patch >= required[2]


def SDL_VERSIONNUM(major, minor, patch):
    """Turn the version numbers into a numeric value.

    For example::

        >>> SDL_VERSIONNUM(1, 2, 3)
        1203

    :Parameters:
     - `major`: int
     - `minor`: int
     - `patch`: int

    :rtype: int
    """
    return x * 1000 + y * 100 + z


SDL_Linked_Version = dll.function('SDL_Linked_Version',
  'Get the version of the dynamically linked SDL library.\n\n    :rtype: `SDL_version`\n    ',
  args=[], arg_types=[], return_type=(POINTER(SDL_version)),
  dereference_return=True,
  require_return=True)

def SDL_VERSION_ATLEAST(major, minor, patch):
    """Determine if the SDL library is at least the given version.

    :Parameters:
     - `major`: int
     - `minor`: int
     - `patch`: int

    :rtype: bool
    """
    v = SDL_Linked_Version()
    return SDL_VERSIONNUM(v.major, v.minor, v.patch) >= SDL_VERSIONNUM(major, minor, patch)