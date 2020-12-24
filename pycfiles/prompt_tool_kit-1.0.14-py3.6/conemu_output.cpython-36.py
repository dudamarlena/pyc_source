# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/terminal/conemu_output.py
# Compiled at: 2019-08-15 23:53:39
# Size of source mod 2**32: 1395 bytes
from __future__ import unicode_literals
from prompt_tool_kit.renderer import Output
from .win32_output import Win32Output
from .vt100_output import Vt100_Output
__all__ = ('ConEmuOutput', )

class ConEmuOutput(object):
    __doc__ = '\n    ConEmu (Windows) output abstraction.\n\n    ConEmu is a Windows console application, but it also supports ANSI escape\n    sequences. This output class is actually a proxy to both `Win32Output` and\n    `Vt100_Output`. It uses `Win32Output` for console sizing and scrolling, but\n    all cursor movements and scrolling happens through the `Vt100_Output`.\n\n    This way, we can have 256 colors in ConEmu and Cmder. Rendering will be\n    even a little faster as well.\n\n    http://conemu.github.io/\n    http://gooseberrycreative.com/cmder/\n    '

    def __init__(self, stdout):
        self.win32_output = Win32Output(stdout)
        self.vt100_output = Vt100_Output(stdout, lambda : None)

    def __getattr__(self, name):
        if name in ('get_size', 'get_rows_below_cursor_position', 'enable_mouse_support',
                    'disable_mouse_support', 'scroll_buffer_to_prompt', 'get_win32_screen_buffer_info',
                    'enable_bracketed_paste', 'disable_bracketed_paste'):
            return getattr(self.win32_output, name)
        else:
            return getattr(self.vt100_output, name)


Output.register(ConEmuOutput)