# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/terminal/conemu_output.py
# Compiled at: 2019-08-15 23:53:39
# Size of source mod 2**32: 1395 bytes
from __future__ import unicode_literals
from prompt_tool_kit.renderer import Output
from .win32_output import Win32Output
from .vt100_output import Vt100_Output
__all__ = ('ConEmuOutput', )

class ConEmuOutput(object):
    """ConEmuOutput"""

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