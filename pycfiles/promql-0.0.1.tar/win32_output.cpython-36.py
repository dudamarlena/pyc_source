# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/terminal/win32_output.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 19614 bytes
from __future__ import unicode_literals
from ctypes import windll, byref, ArgumentError, c_char, c_long, c_ulong, c_uint, pointer
from ctypes.wintypes import DWORD
from prompt_tool_kit.renderer import Output
from prompt_tool_kit.styles import ANSI_COLOR_NAMES
from prompt_tool_kit.win32_types import CONSOLE_SCREEN_BUFFER_INFO, STD_OUTPUT_HANDLE, STD_INPUT_HANDLE, COORD, SMALL_RECT
import os, six
__all__ = ('Win32Output', )

def _coord_byval(coord):
    """
    Turns a COORD object into a c_long.
    This will cause it to be passed by value instead of by reference. (That is what I think at least.)

    When runing ``ptipython`` is run (only with IPython), we often got the following error::

         Error in 'SetConsoleCursorPosition'.
         ArgumentError("argument 2: <class 'TypeError'>: wrong type",)
     argument 2: <class 'TypeError'>: wrong type

    It was solved by turning ``COORD`` parameters into a ``c_long`` like this.

    More info: http://msdn.microsoft.com/en-us/library/windows/desktop/ms686025(v=vs.85).aspx
    """
    return c_long(coord.Y * 65536 | coord.X & 65535)


_DEBUG_RENDER_OUTPUT = False
_DEBUG_RENDER_OUTPUT_FILENAME = 'prompt-toolkit-windows-output.log'

class NoConsoleScreenBufferError(Exception):
    """NoConsoleScreenBufferError"""

    def __init__(self):
        xterm = 'xterm' in os.environ.get('TERM', '')
        if xterm:
            message = 'Found %s, while expecting a Windows console. Maybe try to run this program using "winpty" or run it in cmd.exe instead. Or otherwise, in case of Cygwin, use the Python executable that is compiled for Cygwin.' % os.environ['TERM']
        else:
            message = 'No Windows console found. Are you running cmd.exe?'
        super(NoConsoleScreenBufferError, self).__init__(message)


class Win32Output(Output):
    """Win32Output"""

    def __init__(self, stdout, use_complete_width=False):
        self.use_complete_width = use_complete_width
        self._buffer = []
        self.stdout = stdout
        self.hconsole = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        self._in_alternate_screen = False
        self.color_lookup_table = ColorLookupTable()
        info = self.get_win32_screen_buffer_info()
        self.default_attrs = info.wAttributes if info else 15
        if _DEBUG_RENDER_OUTPUT:
            self.LOG = open(_DEBUG_RENDER_OUTPUT_FILENAME, 'ab')

    def fileno(self):
        """ Return file descriptor. """
        return self.stdout.fileno()

    def encoding(self):
        """ Return encoding used for stdout. """
        return self.stdout.encoding

    def write(self, data):
        self._buffer.append(data)

    def write_raw(self, data):
        """ For win32, there is no difference between write and write_raw. """
        self.write(data)

    def get_size(self):
        from prompt_tool_kit.layout.screen import Size
        info = self.get_win32_screen_buffer_info()
        if self.use_complete_width:
            width = info.dwSize.X
        else:
            width = info.srWindow.Right - info.srWindow.Left
        height = info.srWindow.Bottom - info.srWindow.Top + 1
        maxwidth = info.dwSize.X - 1
        width = min(maxwidth, width)
        return Size(rows=height, columns=width)

    def _winapi(self, func, *a, **kw):
        """
        Flush and call win API function.
        """
        self.flush()
        if _DEBUG_RENDER_OUTPUT:
            self.LOG.write(('%r' % func.__name__).encode('utf-8') + '\n')
            self.LOG.write('     ' + ', '.join(['%r' % i for i in a]).encode('utf-8') + '\n')
            self.LOG.write('     ' + ', '.join(['%r' % type(i) for i in a]).encode('utf-8') + '\n')
            self.LOG.flush()
        try:
            return func(*a, **kw)
        except ArgumentError as e:
            if _DEBUG_RENDER_OUTPUT:
                self.LOG.write(('    Error in %r %r %s\n' % (func.__name__, e, e)).encode('utf-8'))

    def get_win32_screen_buffer_info(self):
        """
        Return Screen buffer info.
        """
        self.flush()
        sbinfo = CONSOLE_SCREEN_BUFFER_INFO()
        success = windll.kernel32.GetConsoleScreenBufferInfo(self.hconsole, byref(sbinfo))
        if success:
            return sbinfo
        raise NoConsoleScreenBufferError

    def set_title(self, title):
        """
        Set terminal title.
        """
        assert isinstance(title, six.text_type)
        self._winapi(windll.kernel32.SetConsoleTitleW, title)

    def clear_title(self):
        self._winapi(windll.kernel32.SetConsoleTitleW, '')

    def erase_screen(self):
        start = COORD(0, 0)
        sbinfo = self.get_win32_screen_buffer_info()
        length = sbinfo.dwSize.X * sbinfo.dwSize.Y
        self.cursor_goto(row=0, column=0)
        self._erase(start, length)

    def erase_down(self):
        sbinfo = self.get_win32_screen_buffer_info()
        size = sbinfo.dwSize
        start = sbinfo.dwCursorPosition
        length = size.X - size.X + size.X * (size.Y - sbinfo.dwCursorPosition.Y)
        self._erase(start, length)

    def erase_end_of_line(self):
        """
        """
        sbinfo = self.get_win32_screen_buffer_info()
        start = sbinfo.dwCursorPosition
        length = sbinfo.dwSize.X - sbinfo.dwCursorPosition.X
        self._erase(start, length)

    def _erase(self, start, length):
        chars_written = c_ulong()
        self._winapi(windll.kernel32.FillConsoleOutputCharacterA, self.hconsole, c_char(' '), DWORD(length), _coord_byval(start), byref(chars_written))
        sbinfo = self.get_win32_screen_buffer_info()
        self._winapi(windll.kernel32.FillConsoleOutputAttribute, self.hconsole, sbinfo.wAttributes, length, _coord_byval(start), byref(chars_written))

    def reset_attributes(self):
        """ Reset the console foreground/background color. """
        self._winapi(windll.kernel32.SetConsoleTextAttribute, self.hconsole, self.default_attrs)

    def set_attributes(self, attrs):
        fgcolor, bgcolor, bold, underline, italic, blink, reverse = attrs
        attrs = self.default_attrs
        if fgcolor is not None:
            attrs = attrs & -16
            attrs |= self.color_lookup_table.lookup_fg_color(fgcolor)
        if bgcolor is not None:
            attrs = attrs & -241
            attrs |= self.color_lookup_table.lookup_bg_color(bgcolor)
        if reverse:
            attrs = attrs & -256 | (attrs & 15) << 4 | (attrs & 240) >> 4
        self._winapi(windll.kernel32.SetConsoleTextAttribute, self.hconsole, attrs)

    def disable_autowrap(self):
        pass

    def enable_autowrap(self):
        pass

    def cursor_goto(self, row=0, column=0):
        pos = COORD(x=column, y=row)
        self._winapi(windll.kernel32.SetConsoleCursorPosition, self.hconsole, _coord_byval(pos))

    def cursor_up(self, amount):
        sr = self.get_win32_screen_buffer_info().dwCursorPosition
        pos = COORD(sr.X, sr.Y - amount)
        self._winapi(windll.kernel32.SetConsoleCursorPosition, self.hconsole, _coord_byval(pos))

    def cursor_down(self, amount):
        self.cursor_up(-amount)

    def cursor_forward(self, amount):
        sr = self.get_win32_screen_buffer_info().dwCursorPosition
        pos = COORD(max(0, sr.X + amount), sr.Y)
        self._winapi(windll.kernel32.SetConsoleCursorPosition, self.hconsole, _coord_byval(pos))

    def cursor_backward(self, amount):
        self.cursor_forward(-amount)

    def flush(self):
        """
        Write to output stream and flush.
        """
        if not self._buffer:
            self.stdout.flush()
            return
        data = ''.join(self._buffer)
        if _DEBUG_RENDER_OUTPUT:
            self.LOG.write(('%r' % data).encode('utf-8') + '\n')
            self.LOG.flush()
        for b in data:
            written = DWORD()
            retval = windll.kernel32.WriteConsoleW(self.hconsole, b, 1, byref(written), None)
            assert retval != 0

        self._buffer = []

    def get_rows_below_cursor_position(self):
        info = self.get_win32_screen_buffer_info()
        return info.srWindow.Bottom - info.dwCursorPosition.Y + 1

    def scroll_buffer_to_prompt(self):
        """
        To be called before drawing the prompt. This should scroll the console
        to left, with the cursor at the bottom (if possible).
        """
        info = self.get_win32_screen_buffer_info()
        sr = info.srWindow
        cursor_pos = info.dwCursorPosition
        result = SMALL_RECT()
        result.Left = 0
        result.Right = sr.Right - sr.Left
        win_height = sr.Bottom - sr.Top
        if 0 < sr.Bottom - cursor_pos.Y < win_height - 1:
            result.Bottom = sr.Bottom
        else:
            result.Bottom = max(win_height, cursor_pos.Y)
        result.Top = result.Bottom - win_height
        self._winapi(windll.kernel32.SetConsoleWindowInfo, self.hconsole, True, byref(result))

    def enter_alternate_screen(self):
        """
        Go to alternate screen buffer.
        """
        if not self._in_alternate_screen:
            GENERIC_READ = 2147483648
            GENERIC_WRITE = 1073741824
            handle = self._winapi(windll.kernel32.CreateConsoleScreenBuffer, GENERIC_READ | GENERIC_WRITE, DWORD(0), None, DWORD(1), None)
            self._winapi(windll.kernel32.SetConsoleActiveScreenBuffer, handle)
            self.hconsole = handle
            self._in_alternate_screen = True

    def quit_alternate_screen(self):
        """
        Make stdout again the active buffer.
        """
        if self._in_alternate_screen:
            stdout = self._winapi(windll.kernel32.GetStdHandle, STD_OUTPUT_HANDLE)
            self._winapi(windll.kernel32.SetConsoleActiveScreenBuffer, stdout)
            self._winapi(windll.kernel32.CloseHandle, self.hconsole)
            self.hconsole = stdout
            self._in_alternate_screen = False

    def enable_mouse_support(self):
        ENABLE_MOUSE_INPUT = 16
        handle = windll.kernel32.GetStdHandle(STD_INPUT_HANDLE)
        original_mode = DWORD()
        self._winapi(windll.kernel32.GetConsoleMode, handle, pointer(original_mode))
        self._winapi(windll.kernel32.SetConsoleMode, handle, original_mode.value | ENABLE_MOUSE_INPUT)

    def disable_mouse_support(self):
        ENABLE_MOUSE_INPUT = 16
        handle = windll.kernel32.GetStdHandle(STD_INPUT_HANDLE)
        original_mode = DWORD()
        self._winapi(windll.kernel32.GetConsoleMode, handle, pointer(original_mode))
        self._winapi(windll.kernel32.SetConsoleMode, handle, original_mode.value & ~ENABLE_MOUSE_INPUT)

    def hide_cursor(self):
        pass

    def show_cursor(self):
        pass

    @classmethod
    def win32_refresh_window(cls):
        """
        Call win32 API to refresh the whole Window.

        This is sometimes necessary when the application paints background
        for completion menus. When the menu disappears, it leaves traces due
        to a bug in the Windows Console. Sending a repaint request solves it.
        """
        handle = windll.kernel32.GetConsoleWindow()
        RDW_INVALIDATE = 1
        windll.user32.RedrawWindow(handle, None, None, c_uint(RDW_INVALIDATE))


class FOREGROUND_COLOR:
    BLACK = 0
    BLUE = 1
    GREEN = 2
    CYAN = 3
    RED = 4
    MAGENTA = 5
    YELLOW = 6
    GRAY = 7
    INTENSITY = 8


class BACKROUND_COLOR:
    BLACK = 0
    BLUE = 16
    GREEN = 32
    CYAN = 48
    RED = 64
    MAGENTA = 80
    YELLOW = 96
    GRAY = 112
    INTENSITY = 128


def _create_ansi_color_dict(color_cls):
    """ Create a table that maps the 16 named ansi colors to their Windows code. """
    return {'ansidefault':color_cls.BLACK, 
     'ansiblack':color_cls.BLACK, 
     'ansidarkgray':color_cls.BLACK | color_cls.INTENSITY, 
     'ansilightgray':color_cls.GRAY, 
     'ansiwhite':color_cls.GRAY | color_cls.INTENSITY, 
     'ansidarkred':color_cls.RED, 
     'ansidarkgreen':color_cls.GREEN, 
     'ansibrown':color_cls.YELLOW, 
     'ansidarkblue':color_cls.BLUE, 
     'ansipurple':color_cls.MAGENTA, 
     'ansiteal':color_cls.CYAN, 
     'ansired':color_cls.RED | color_cls.INTENSITY, 
     'ansigreen':color_cls.GREEN | color_cls.INTENSITY, 
     'ansiyellow':color_cls.YELLOW | color_cls.INTENSITY, 
     'ansiblue':color_cls.BLUE | color_cls.INTENSITY, 
     'ansifuchsia':color_cls.MAGENTA | color_cls.INTENSITY, 
     'ansiturquoise':color_cls.CYAN | color_cls.INTENSITY}


FG_ANSI_COLORS = _create_ansi_color_dict(FOREGROUND_COLOR)
BG_ANSI_COLORS = _create_ansi_color_dict(BACKROUND_COLOR)
if not set(FG_ANSI_COLORS) == set(ANSI_COLOR_NAMES):
    raise AssertionError
elif not set(BG_ANSI_COLORS) == set(ANSI_COLOR_NAMES):
    raise AssertionError

class ColorLookupTable(object):
    """ColorLookupTable"""

    def __init__(self):
        self._win32_colors = self._build_color_table()
        self.best_match = {}

    @staticmethod
    def _build_color_table():
        """
        Build an RGB-to-256 color conversion table
        """
        FG = FOREGROUND_COLOR
        BG = BACKROUND_COLOR
        return [
         (
          0, 0, 0, FG.BLACK, BG.BLACK),
         (
          0, 0, 170, FG.BLUE, BG.BLUE),
         (
          0, 170, 0, FG.GREEN, BG.GREEN),
         (
          0, 170, 170, FG.CYAN, BG.CYAN),
         (
          170, 0, 0, FG.RED, BG.RED),
         (
          170, 0, 170, FG.MAGENTA, BG.MAGENTA),
         (
          170, 170, 0, FG.YELLOW, BG.YELLOW),
         (
          136, 136, 136, FG.GRAY, BG.GRAY),
         (
          68, 68, 255, FG.BLUE | FG.INTENSITY, BG.BLUE | BG.INTENSITY),
         (
          68, 255, 68, FG.GREEN | FG.INTENSITY, BG.GREEN | BG.INTENSITY),
         (
          68, 255, 255, FG.CYAN | FG.INTENSITY, BG.CYAN | BG.INTENSITY),
         (
          255, 68, 68, FG.RED | FG.INTENSITY, BG.RED | BG.INTENSITY),
         (
          255, 68, 255, FG.MAGENTA | FG.INTENSITY, BG.MAGENTA | BG.INTENSITY),
         (
          255, 255, 68, FG.YELLOW | FG.INTENSITY, BG.YELLOW | BG.INTENSITY),
         (
          68, 68, 68, FG.BLACK | FG.INTENSITY, BG.BLACK | BG.INTENSITY),
         (
          255, 255, 255, FG.GRAY | FG.INTENSITY, BG.GRAY | BG.INTENSITY)]

    def _closest_color(self, r, g, b):
        distance = 198147
        fg_match = 0
        bg_match = 0
        for r_, g_, b_, fg_, bg_ in self._win32_colors:
            rd = r - r_
            gd = g - g_
            bd = b - b_
            d = rd * rd + gd * gd + bd * bd
            if d < distance:
                fg_match = fg_
                bg_match = bg_
                distance = d

        return (
         fg_match, bg_match)

    def _color_indexes(self, color):
        indexes = self.best_match.get(color, None)
        if indexes is None:
            try:
                rgb = int(str(color), 16)
            except ValueError:
                rgb = 0

            r = rgb >> 16 & 255
            g = rgb >> 8 & 255
            b = rgb & 255
            indexes = self._closest_color(r, g, b)
            self.best_match[color] = indexes
        return indexes

    def lookup_fg_color(self, fg_color):
        """
        Return the color for use in the
        `windll.kernel32.SetConsoleTextAttribute` API call.

        :param fg_color: Foreground as text. E.g. 'ffffff' or 'red'
        """
        if fg_color in FG_ANSI_COLORS:
            return FG_ANSI_COLORS[fg_color]
        else:
            return self._color_indexes(fg_color)[0]

    def lookup_bg_color(self, bg_color):
        """
        Return the color for use in the
        `windll.kernel32.SetConsoleTextAttribute` API call.

        :param bg_color: Background as text. E.g. 'ffffff' or 'red'
        """
        if bg_color in BG_ANSI_COLORS:
            return BG_ANSI_COLORS[bg_color]
        else:
            return self._color_indexes(bg_color)[1]