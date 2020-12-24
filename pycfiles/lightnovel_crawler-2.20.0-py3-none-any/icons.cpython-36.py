# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/assets/icons.py
# Compiled at: 2020-03-05 23:56:06
# Size of source mod 2**32: 780 bytes
import platform
isMac = platform.system() == 'Darwin'
isLinux = platform.system() == 'Linux'
isWindows = platform.system() == 'Windows'

class Icons:
    isMac = isMac
    isLinux = isLinux
    isWindows = isWindows
    hasSupport = isLinux or isMac
    EMPTY = '  '
    BOOK = '📒' if hasSupport else ''
    CLOVER = '🍀' if hasSupport else '#'
    LINK = '🔗' if hasSupport else '-'
    HANDS = '🙏' if hasSupport else '-'
    ERROR = '❗' if hasSupport else '!'
    PARTY = '📦' if hasSupport else '$'
    SOUND = '🔊' if hasSupport else '<<'
    SPARKLE = '✨' if hasSupport else '*'
    INFO = '💁  ' if hasSupport else ': '
    RIGHT_ARROW = '➡' if hasSupport else '->'