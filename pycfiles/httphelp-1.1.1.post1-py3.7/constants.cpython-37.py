# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\httphelp\constants.py
# Compiled at: 2018-11-27 07:12:25
# Size of source mod 2**32: 551 bytes
import os
CURR_DIR = os.path.dirname(os.path.realpath(__file__))
_isNotDumb = os.getenv('TERM', 'dumb').lower() != 'dumb'
SCROLL_LINE_UP = 'line up'
SCROLL_LINE_DOWN = 'line down'
SCROLL_PAGE_UP = 'page up'
SCROLL_PAGE_DOWN = 'page down'
SCROLL_TO_TOP = 'to top'
SCROLL_TO_END = 'to end'
YELLOW = '\x1b[33m' if _isNotDumb else ''
RED = '\x1b[31m' if _isNotDumb else ''
BOLD = '\x1b[1m' if _isNotDumb else ''
UNDERLINE = '\x1b[4m' if _isNotDumb else ''
END = '\x1b[0m' if _isNotDumb else ''