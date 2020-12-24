# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: d:\dev\cocos2020\cocos\audio\SDL\error.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1814 bytes
__doc__ = 'Error detection and error handling functions.\n'
__docformat__ = 'restructuredtext'
__version__ = '$Id: $'
from ctypes import *
from . import dll

class SDL_Exception(Exception):
    """SDL_Exception"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class SDL_NotImplementedError(NotImplementedError):
    """SDL_NotImplementedError"""
    pass


SDL_SetError = dll.function('SDL_SetError', 'Set the static error string.\n\n                            :Parameters:\n                                `fmt`\n                                    format string; subsequent integer and string arguments are\n                                    interpreted as in printf().\n                            ',
  args=[
 'fmt'],
  arg_types=[
 c_char_p],
  return_type=None)
SDL_GetError = dll.function('SDL_GetError', 'Return the last error string set.\n\n                            :rtype: string\n                            ',
  args=[], arg_types=[], return_type=c_char_p)
SDL_ClearError = dll.function('SDL_ClearError', 'Clear any error string set.\n                              ',
  args=[], arg_types=[], return_type=None)