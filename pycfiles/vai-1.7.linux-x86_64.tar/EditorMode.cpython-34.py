# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/EditorMode.py
# Compiled at: 2014-12-14 06:26:18
# Size of source mod 2**32: 1091 bytes


class EditorMode:
    __doc__ = '\n    Separate enum class to hold the current editor mode\n    '
    COMMAND = 0
    COMMAND_INPUT = 1
    INSERT = 2
    REPLACE = 3
    VISUAL_BLOCK = 4
    VISUAL_LINE = 5
    VISUAL = 6
    DELETE = 7
    SEARCH_FORWARD = 8
    SEARCH_BACKWARD = 9
    GO = 10
    YANK = 11
    ZETA = 12
    BOOKMARK = 13
    GOTOBOOKMARK = 14