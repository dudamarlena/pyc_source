# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: d:\dev\cocos2020\cocos\audio\SDL\endian.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1096 bytes
__doc__ = 'Functions for converting to native byte order\n'
__docformat__ = 'restructuredtext'
__version__ = '$Id: $'
import sys
from cocos.audio.SDL.constants import SDL_BIG_ENDIAN, SDL_LIL_ENDIAN

def SDL_Swap16(x):
    return x << 8 & 65280 | x >> 8 & 255


def SDL_Swap32(x):
    return x << 24 & 4278190080 | x << 8 & 16711680 | x >> 8 & 65280 | x >> 24 & 255


def SDL_Swap64(x):
    return SDL_Swap32(x & 4294967295) << 32 | SDL_Swap32(x >> 32 & 4294967295)


def _noop(x):
    return x


if sys.byteorder == 'big':
    SDL_BYTEORDER = SDL_BIG_ENDIAN
    SDL_SwapLE16 = SDL_Swap16
    SDL_SwapLE32 = SDL_Swap32
    SDL_SwapLE64 = SDL_Swap64
    SDL_SwapBE16 = _noop
    SDL_SwapBE32 = _noop
    SDL_SwapBE64 = _noop
else:
    SDL_BYTEORDER = SDL_LIL_ENDIAN
    SDL_SwapLE16 = _noop
    SDL_SwapLE32 = _noop
    SDL_SwapLE64 = _noop
    SDL_SwapBE16 = SDL_Swap16
    SDL_SwapBE32 = SDL_Swap32
    SDL_SwapBE64 = SDL_Swap64