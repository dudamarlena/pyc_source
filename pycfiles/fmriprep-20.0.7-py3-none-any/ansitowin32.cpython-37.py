# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/pip/pip/_vendor/colorama/ansitowin32.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 10462 bytes
import re, sys, os
from .ansi import AnsiFore, AnsiBack, AnsiStyle, Style
from .winterm import WinTerm, WinColor, WinStyle
from .win32 import windll, winapi_test
winterm = None
if windll is not None:
    winterm = WinTerm()

class StreamWrapper(object):
    __doc__ = "\n    Wraps a stream (such as stdout), acting as a transparent proxy for all\n    attribute access apart from method 'write()', which is delegated to our\n    Converter instance.\n    "

    def __init__(self, wrapped, converter):
        self._StreamWrapper__wrapped = wrapped
        self._StreamWrapper__convertor = converter

    def __getattr__(self, name):
        return getattr(self._StreamWrapper__wrapped, name)

    def __enter__(self, *args, **kwargs):
        return (self._StreamWrapper__wrapped.__enter__)(*args, **kwargs)

    def __exit__(self, *args, **kwargs):
        return (self._StreamWrapper__wrapped.__exit__)(*args, **kwargs)

    def write(self, text):
        self._StreamWrapper__convertor.write(text)

    def isatty(self):
        stream = self._StreamWrapper__wrapped
        if 'PYCHARM_HOSTED' in os.environ:
            if stream is not None:
                if stream is sys.__stdout__ or stream is sys.__stderr__:
                    return True
        try:
            stream_isatty = stream.isatty
        except AttributeError:
            return False
        else:
            return stream_isatty()

    @property
    def closed(self):
        stream = self._StreamWrapper__wrapped
        try:
            return stream.closed
        except AttributeError:
            return True


class AnsiToWin32(object):
    __doc__ = "\n    Implements a 'write()' method which, on Windows, will strip ANSI character\n    sequences from the text, and if outputting to a tty, will convert them into\n    win32 function calls.\n    "
    ANSI_CSI_RE = re.compile('\x01?\x1b\\[((?:\\d|;)*)([a-zA-Z])\x02?')
    ANSI_OSC_RE = re.compile('\x01?\x1b\\]((?:.|;)*?)(\x07)\x02?')

    def __init__(self, wrapped, convert=None, strip=None, autoreset=False):
        self.wrapped = wrapped
        self.autoreset = autoreset
        self.stream = StreamWrapper(wrapped, self)
        on_windows = os.name == 'nt'
        conversion_supported = on_windows and winapi_test()
        if strip is None:
            strip = conversion_supported or not self.stream.closed and not self.stream.isatty()
        self.strip = strip
        if convert is None:
            convert = conversion_supported and not self.stream.closed and self.stream.isatty()
        self.convert = convert
        self.win32_calls = self.get_win32_calls()
        self.on_stderr = self.wrapped is sys.stderr

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
        if self.convert:
            if winterm:
                return {AnsiStyle.RESET_ALL: (winterm.reset_all,), 
                 AnsiStyle.BRIGHT: (winterm.style, WinStyle.BRIGHT), 
                 AnsiStyle.DIM: (winterm.style, WinStyle.NORMAL), 
                 AnsiStyle.NORMAL: (winterm.style, WinStyle.NORMAL), 
                 AnsiFore.BLACK: (winterm.fore, WinColor.BLACK), 
                 AnsiFore.RED: (winterm.fore, WinColor.RED), 
                 AnsiFore.GREEN: (winterm.fore, WinColor.GREEN), 
                 AnsiFore.YELLOW: (winterm.fore, WinColor.YELLOW), 
                 AnsiFore.BLUE: (winterm.fore, WinColor.BLUE), 
                 AnsiFore.MAGENTA: (winterm.fore, WinColor.MAGENTA), 
                 AnsiFore.CYAN: (winterm.fore, WinColor.CYAN), 
                 AnsiFore.WHITE: (winterm.fore, WinColor.GREY), 
                 AnsiFore.RESET: (winterm.fore,), 
                 AnsiFore.LIGHTBLACK_EX: (winterm.fore, WinColor.BLACK, True), 
                 AnsiFore.LIGHTRED_EX: (winterm.fore, WinColor.RED, True), 
                 AnsiFore.LIGHTGREEN_EX: (winterm.fore, WinColor.GREEN, True), 
                 AnsiFore.LIGHTYELLOW_EX: (winterm.fore, WinColor.YELLOW, True), 
                 AnsiFore.LIGHTBLUE_EX: (winterm.fore, WinColor.BLUE, True), 
                 AnsiFore.LIGHTMAGENTA_EX: (winterm.fore, WinColor.MAGENTA, True), 
                 AnsiFore.LIGHTCYAN_EX: (winterm.fore, WinColor.CYAN, True), 
                 AnsiFore.LIGHTWHITE_EX: (winterm.fore, WinColor.GREY, True), 
                 AnsiBack.BLACK: (winterm.back, WinColor.BLACK), 
                 AnsiBack.RED: (winterm.back, WinColor.RED), 
                 AnsiBack.GREEN: (winterm.back, WinColor.GREEN), 
                 AnsiBack.YELLOW: (winterm.back, WinColor.YELLOW), 
                 AnsiBack.BLUE: (winterm.back, WinColor.BLUE), 
                 AnsiBack.MAGENTA: (winterm.back, WinColor.MAGENTA), 
                 AnsiBack.CYAN: (winterm.back, WinColor.CYAN), 
                 AnsiBack.WHITE: (winterm.back, WinColor.GREY), 
                 AnsiBack.RESET: (winterm.back,), 
                 AnsiBack.LIGHTBLACK_EX: (winterm.back, WinColor.BLACK, True), 
                 AnsiBack.LIGHTRED_EX: (winterm.back, WinColor.RED, True), 
                 AnsiBack.LIGHTGREEN_EX: (winterm.back, WinColor.GREEN, True), 
                 AnsiBack.LIGHTYELLOW_EX: (winterm.back, WinColor.YELLOW, True), 
                 AnsiBack.LIGHTBLUE_EX: (winterm.back, WinColor.BLUE, True), 
                 AnsiBack.LIGHTMAGENTA_EX: (winterm.back, WinColor.MAGENTA, True), 
                 AnsiBack.LIGHTCYAN_EX: (winterm.back, WinColor.CYAN, True), 
                 AnsiBack.LIGHTWHITE_EX: (winterm.back, WinColor.GREY, True)}
        return dict()

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
        else:
            if not self.strip:
                if not self.stream.closed:
                    self.wrapped.write(Style.RESET_ALL)

    def write_and_convert(self, text):
        """
        Write the given text to our wrapped stream, stripping any ANSI
        sequences from the text, and optionally converting them into win32
        calls.
        """
        cursor = 0
        text = self.convert_osc(text)
        for match in self.ANSI_CSI_RE.finditer(text):
            start, end = match.span()
            self.write_plain_text(text, cursor, start)
            (self.convert_ansi)(*match.groups())
            cursor = end

        self.write_plain_text(text, cursor, len(text))

    def write_plain_text(self, text, start, end):
        if start < end:
            self.wrapped.write(text[start:end])
            self.wrapped.flush()

    def convert_ansi(self, paramstring, command):
        if self.convert:
            params = self.extract_params(command, paramstring)
            self.call_win32(command, params)

    def extract_params(self, command, paramstring):
        if command in 'Hf':
            params = tuple(((int(p) if len(p) != 0 else 1) for p in paramstring.split(';')))
            while len(params) < 2:
                params = params + (1, )

        else:
            params = tuple((int(p) for p in paramstring.split(';') if len(p) != 0))
            if len(params) == 0:
                if command in 'JKm':
                    params = (0, )
                else:
                    if command in 'ABCD':
                        params = (1, )
        return params

    def call_win32(self, command, params):
        if command == 'm':
            for param in params:
                if param in self.win32_calls:
                    func_args = self.win32_calls[param]
                    func = func_args[0]
                    args = func_args[1:]
                    kwargs = dict(on_stderr=(self.on_stderr))
                    func(*args, **kwargs)

        else:
            if command in 'J':
                winterm.erase_screen((params[0]), on_stderr=(self.on_stderr))
            else:
                if command in 'K':
                    winterm.erase_line((params[0]), on_stderr=(self.on_stderr))
                else:
                    if command in 'Hf':
                        winterm.set_cursor_position(params, on_stderr=(self.on_stderr))
                    else:
                        if command in 'ABCD':
                            n = params[0]
                            x, y = {'A':(
                              0, -n), 
                             'B':(0, n),  'C':(n, 0),  'D':(-n, 0)}[command]
                            winterm.cursor_adjust(x, y, on_stderr=(self.on_stderr))

    def convert_osc(self, text):
        for match in self.ANSI_OSC_RE.finditer(text):
            start, end = match.span()
            text = text[:start] + text[end:]
            paramstring, command = match.groups()
            if command in '\x07':
                params = paramstring.split(';')
                if params[0] in '02':
                    winterm.set_title(params[1])

        return text