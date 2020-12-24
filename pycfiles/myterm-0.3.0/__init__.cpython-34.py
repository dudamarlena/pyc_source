# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\faoustin\Downloads\myterm\myterm\__init__.py
# Compiled at: 2016-10-05 09:01:06
# Size of source mod 2**32: 4239 bytes
"""
    Module myterm
"""
import os, sys, colorconsole, colorconsole.terminal
__version_info__ = (0, 3, 0)
__version__ = '.'.join([str(val) for val in __version_info__])
try:
    if os.name == 'posix':
        import colorconsole.ansi

        class Terminal(colorconsole.ansi.Terminal):
            __doc__ = '\n                class Terminal ansi with set_color, clean\n            '
            colors_fg = {0: '30m', 
             1: '34m', 
             2: '32m', 
             3: '36m', 
             4: '31m', 
             5: '35m', 
             6: '33m', 
             7: '37m', 
             8: '1;30m', 
             9: '1;34m', 
             10: '1;32m', 
             11: '1;36m', 
             12: '1;31m', 
             13: '1;35m', 
             14: '1;33m', 
             15: '1;37m'}
            colors_bk = {0: '40m', 
             1: '44m', 
             2: '42m', 
             3: '46m', 
             4: '41m', 
             5: '45m', 
             6: '43m', 
             7: '47m'}

            def __init__(self, **kw):
                colorconsole.ansi.Terminal.__init__(self, **kw)

            def set_color(self, fg=None, bk=None, stream=sys.stdout):
                if fg is not None:
                    stream.write(Terminal.escape + self.colors_fg[fg])
                if bk is not None:
                    stream.write(Terminal.escape + self.colors_bk[bk])

            def clean(self, stream=sys.stdout):
                """ clean stream"""
                stream.write('\x1b[0m')


        SCREEN = Terminal()
        FOREGROUND_DEFAULT = None
        BACKGROUND_DEFAULT = None
    else:
        import colorconsole.win

        class Terminal(colorconsole.win.Terminal):
            __doc__ = '\n                class Terminal win with set_color, clean\n            '

            def __init__(self, **kw):
                colorconsole.win.Terminal.__init__(self, **kw)

            def set_color(self, fg=None, bk=None, stream=sys.stdout):
                colorconsole.win.Terminal.set_color(self, fg, bk)

            def clean(self, stream=sys.stdout):
                """ clean stream"""
                pass


        SCREEN = Terminal()
        FOREGROUND_DEFAULT = colorconsole.terminal.colors['WHITE']
        BACKGROUND_DEFAULT = colorconsole.terminal.colors['BLACK']
except Exception as ex:

    class Terminal(object):
        __doc__ = '\n            class Terminal minimal with set_color, clean\n        '

        def __init__(self, **kw):
            pass

        def set_color(self, fg=None, bk=None, stream=sys.stdout):
            """ clean stream"""
            pass

        def clean(self, stream=sys.stdout):
            """ clean stream"""
            pass


    SCREEN = Terminal()
    FOREGROUND_DEFAULT = colorconsole.terminal.colors['WHITE']
    BACKGROUND_DEFAULT = colorconsole.terminal.colors['BLACK']

FOREGROUND_CRITICAL = colorconsole.terminal.colors['RED']
BACKGROUND_CRITICAL = BACKGROUND_DEFAULT
FOREGROUND_ERROR = colorconsole.terminal.colors['PURPLE']
BACKGROUND_ERROR = BACKGROUND_DEFAULT
FOREGROUND_WARNING = colorconsole.terminal.colors['BROWN']
BACKGROUND_WARNING = BACKGROUND_DEFAULT
FOREGROUND_INFO = colorconsole.terminal.colors['GREEN']
BACKGROUND_INFO = BACKGROUND_DEFAULT
FOREGROUND_DEBUG = colorconsole.terminal.colors['BLUE']
BACKGROUND_DEBUG = BACKGROUND_DEFAULT
FOREGROUND_NOSET = FOREGROUND_DEFAULT
BACKGROUND_NOSET = BACKGROUND_DEFAULT
FOREGROUND_PROMPT = colorconsole.terminal.colors['BROWN']
BACKGROUND_PROMPT = BACKGROUND_DEFAULT