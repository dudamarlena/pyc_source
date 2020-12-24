# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/thirdparty/colorama/ansitowin32.py
# Compiled at: 2018-11-28 03:20:09
import re, sys
from .ansi import AnsiFore, AnsiBack, AnsiStyle, Style
from .winterm import WinTerm, WinColor, WinStyle
from .win32 import windll
if windll is not None:
    winterm = WinTerm()

def is_a_tty(stream):
    return hasattr(stream, 'isatty') and stream.isatty()


class StreamWrapper(object):
    """
    Wraps a stream (such as stdout), acting as a transparent proxy for all
    attribute access apart from method 'write()', which is delegated to our
    Converter instance.
    """

    def __init__(self, wrapped, converter):
        self.__wrapped = wrapped
        self.__convertor = converter

    def __getattr__(self, name):
        return getattr(self.__wrapped, name)

    def write(self, text):
        self.__convertor.write(text)


class AnsiToWin32(object):
    """
    Implements a 'write()' method which, on Windows, will strip ANSI character
    sequences from the text, and if outputting to a tty, will convert them into
    win32 function calls.
    """
    ANSI_RE = re.compile('\x1b\\[((?:\\d|;)*)([a-zA-Z])')

    def __init__(self, wrapped, convert=None, strip=None, autoreset=False):
        self.wrapped = wrapped
        self.autoreset = autoreset
        self.stream = StreamWrapper(wrapped, self)
        on_windows = sys.platform.startswith('win')
        if strip is None:
            strip = on_windows
        self.strip = strip
        if convert is None:
            convert = on_windows and is_a_tty(wrapped)
        self.convert = convert
        self.win32_calls = self.get_win32_calls()
        self.on_stderr = self.wrapped is sys.stderr
        return

    def should_wrap(self):
        """
        True if this class is actually needed. If false, then the output
        stream will not be affected, nor will win32 calls be issued, so
        wrapping stdout is not actually required. This will generally be
        False on non-Windows platforms, unless optional functionality like
        autoreset has been requested using kwargs to init()
        """
        return self.convert or self.strip or self.autoreset

    def get_win32_calls(self):
        if self.convert and winterm:
            return {AnsiStyle.RESET_ALL: (
                                   winterm.reset_all,), 
               AnsiStyle.BRIGHT: (
                                winterm.style, WinStyle.BRIGHT), 
               AnsiStyle.DIM: (
                             winterm.style, WinStyle.NORMAL), 
               AnsiStyle.NORMAL: (
                                winterm.style, WinStyle.NORMAL), 
               AnsiFore.BLACK: (
                              winterm.fore, WinColor.BLACK), 
               AnsiFore.RED: (
                            winterm.fore, WinColor.RED), 
               AnsiFore.GREEN: (
                              winterm.fore, WinColor.GREEN), 
               AnsiFore.YELLOW: (
                               winterm.fore, WinColor.YELLOW), 
               AnsiFore.BLUE: (
                             winterm.fore, WinColor.BLUE), 
               AnsiFore.MAGENTA: (
                                winterm.fore, WinColor.MAGENTA), 
               AnsiFore.CYAN: (
                             winterm.fore, WinColor.CYAN), 
               AnsiFore.WHITE: (
                              winterm.fore, WinColor.GREY), 
               AnsiFore.RESET: (
                              winterm.fore,), 
               AnsiBack.BLACK: (
                              winterm.back, WinColor.BLACK), 
               AnsiBack.RED: (
                            winterm.back, WinColor.RED), 
               AnsiBack.GREEN: (
                              winterm.back, WinColor.GREEN), 
               AnsiBack.YELLOW: (
                               winterm.back, WinColor.YELLOW), 
               AnsiBack.BLUE: (
                             winterm.back, WinColor.BLUE), 
               AnsiBack.MAGENTA: (
                                winterm.back, WinColor.MAGENTA), 
               AnsiBack.CYAN: (
                             winterm.back, WinColor.CYAN), 
               AnsiBack.WHITE: (
                              winterm.back, WinColor.GREY), 
               AnsiBack.RESET: (
                              winterm.back,)}

    def write(self, text):
        if self.strip or self.convert:
            self.write_and_convert(text)
        else:
            self.wrapped.write(text)
            self.wrapped.flush()
        if self.autoreset:
            self.reset_all()

    def reset_all(self):
        if self.convert:
            self.call_win32('m', (0, ))
        elif is_a_tty(self.wrapped):
            self.wrapped.write(Style.RESET_ALL)

    def write_and_convert(self, text):
        """
        Write the given text to our wrapped stream, stripping any ANSI
        sequences from the text, and optionally converting them into win32
        calls.
        """
        cursor = 0
        for match in self.ANSI_RE.finditer(text):
            start, end = match.span()
            self.write_plain_text(text, cursor, start)
            self.convert_ansi(*match.groups())
            cursor = end

        self.write_plain_text(text, cursor, len(text))

    def write_plain_text(self, text, start, end):
        if start < end:
            self.wrapped.write(text[start:end])
            self.wrapped.flush()

    def convert_ansi(self, paramstring, command):
        if self.convert:
            params = self.extract_params(paramstring)
            self.call_win32(command, params)

    def extract_params(self, paramstring):

        def split(paramstring):
            for p in paramstring.split(';'):
                if p != '':
                    yield int(p)

        return tuple(split(paramstring))

    def call_win32(self, command, params):
        if params == []:
            params = [
             0]
        if command == 'm':
            for param in params:
                if param in self.win32_calls:
                    func_args = self.win32_calls[param]
                    func = func_args[0]
                    args = func_args[1:]
                    kwargs = dict(on_stderr=self.on_stderr)
                    func(*args, **kwargs)

        elif command in ('H', 'f'):
            func = winterm.set_cursor_position
            func(params, on_stderr=self.on_stderr)
        elif command in 'J':
            func = winterm.erase_data
            func(params, on_stderr=self.on_stderr)
        elif command == 'A':
            if params == () or params == None:
                num_rows = 1
            else:
                num_rows = params[0]
            func = winterm.cursor_up
            func(num_rows, on_stderr=self.on_stderr)
        return