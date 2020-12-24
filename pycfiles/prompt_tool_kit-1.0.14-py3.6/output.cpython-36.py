# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/output.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 5034 bytes
"""
Interface for an output.
"""
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from six import with_metaclass
from prompt_tool_kit.layout.screen import Size
__all__ = ('Output', )

class Output(with_metaclass(ABCMeta, object)):
    __doc__ = '\n    Base class defining the output interface for a\n    :class:`~prompt_tool_kit.renderer.Renderer`.\n\n    Actual implementations are\n    :class:`~prompt_tool_kit.terminal.vt100_output.Vt100_Output` and\n    :class:`~prompt_tool_kit.terminal.win32_output.Win32Output`.\n    '

    @abstractmethod
    def fileno(self):
        """ Return the file descriptor to which we can write for the output. """
        pass

    @abstractmethod
    def encoding(self):
        """
        Return the encoding for this output, e.g. 'utf-8'.
        (This is used mainly to know which characters are supported by the
        output the data, so that the UI can provide alternatives, when
        required.)
        """
        pass

    @abstractmethod
    def write(self, data):
        """ Write text (Terminal escape sequences will be removed/escaped.) """
        pass

    @abstractmethod
    def write_raw(self, data):
        """ Write text. """
        pass

    @abstractmethod
    def set_title(self, title):
        """ Set terminal title. """
        pass

    @abstractmethod
    def clear_title(self):
        """ Clear title again. (or restore previous title.) """
        pass

    @abstractmethod
    def flush(self):
        """ Write to output stream and flush. """
        pass

    @abstractmethod
    def erase_screen(self):
        """
        Erases the screen with the background colour and moves the cursor to
        home.
        """
        pass

    @abstractmethod
    def enter_alternate_screen(self):
        """ Go to the alternate screen buffer. (For full screen applications). """
        pass

    @abstractmethod
    def quit_alternate_screen(self):
        """ Leave the alternate screen buffer. """
        pass

    @abstractmethod
    def enable_mouse_support(self):
        """ Enable mouse. """
        pass

    @abstractmethod
    def disable_mouse_support(self):
        """ Disable mouse. """
        pass

    @abstractmethod
    def erase_end_of_line(self):
        """
        Erases from the current cursor position to the end of the current line.
        """
        pass

    @abstractmethod
    def erase_down(self):
        """
        Erases the screen from the current line down to the bottom of the
        screen.
        """
        pass

    @abstractmethod
    def reset_attributes(self):
        """ Reset color and styling attributes. """
        pass

    @abstractmethod
    def set_attributes(self, attrs):
        """ Set new color and styling attributes. """
        pass

    @abstractmethod
    def disable_autowrap(self):
        """ Disable auto line wrapping. """
        pass

    @abstractmethod
    def enable_autowrap(self):
        """ Enable auto line wrapping. """
        pass

    @abstractmethod
    def cursor_goto(self, row=0, column=0):
        """ Move cursor position. """
        pass

    @abstractmethod
    def cursor_up(self, amount):
        """ Move cursor `amount` place up. """
        pass

    @abstractmethod
    def cursor_down(self, amount):
        """ Move cursor `amount` place down. """
        pass

    @abstractmethod
    def cursor_forward(self, amount):
        """ Move cursor `amount` place forward. """
        pass

    @abstractmethod
    def cursor_backward(self, amount):
        """ Move cursor `amount` place backward. """
        pass

    @abstractmethod
    def hide_cursor(self):
        """ Hide cursor. """
        pass

    @abstractmethod
    def show_cursor(self):
        """ Show cursor. """
        pass

    def ask_for_cpr(self):
        """
        Asks for a cursor position report (CPR).
        (VT100 only.)
        """
        pass

    def bell(self):
        """ Sound bell. """
        pass

    def enable_bracketed_paste(self):
        """ For vt100 only. """
        pass

    def disable_bracketed_paste(self):
        """ For vt100 only. """
        pass


class DummyOutput(Output):
    __doc__ = "\n    For testing. An output class that doesn't render anything.\n    "

    def fileno(self):
        """ There is no sensible default for fileno(). """
        raise NotImplementedError

    def encoding(self):
        return 'utf-8'

    def write(self, data):
        pass

    def write_raw(self, data):
        pass

    def set_title(self, title):
        pass

    def clear_title(self):
        pass

    def flush(self):
        pass

    def erase_screen(self):
        pass

    def enter_alternate_screen(self):
        pass

    def quit_alternate_screen(self):
        pass

    def enable_mouse_support(self):
        pass

    def disable_mouse_support(self):
        pass

    def erase_end_of_line(self):
        pass

    def erase_down(self):
        pass

    def reset_attributes(self):
        pass

    def set_attributes(self, attrs):
        pass

    def disable_autowrap(self):
        pass

    def enable_autowrap(self):
        pass

    def cursor_goto(self, row=0, column=0):
        pass

    def cursor_up(self, amount):
        pass

    def cursor_down(self, amount):
        pass

    def cursor_forward(self, amount):
        pass

    def cursor_backward(self, amount):
        pass

    def hide_cursor(self):
        pass

    def show_cursor(self):
        pass

    def ask_for_cpr(self):
        pass

    def bell(self):
        pass

    def enable_bracketed_paste(self):
        pass

    def disable_bracketed_paste(self):
        pass

    def get_size(self):
        return Size(rows=40, columns=80)