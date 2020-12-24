# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/reporting/colored.py
# Compiled at: 2009-10-07 18:08:46
"""Color text stream reporting"""
import os, sys
ANSI_CODES = {'reset': '\x1b[0m', 'bold': '\x1b[01m', 'teal': '\x1b[36;06m', 'turquoise': '\x1b[36;01m', 'fuscia': '\x1b[35;01m', 'purple': '\x1b[35;06m', 'blue': '\x1b[34;01m', 'darkblue': '\x1b[34;06m', 'green': '\x1b[32;01m', 'darkgreen': '\x1b[32;06m', 'yellow': '\x1b[33;01m', 'brown': '\x1b[33;06m', 'red': '\x1b[31;01m'}
from textstream import StreamWriter

class TerminalColorWriter(StreamWriter):
    __module__ = __name__

    def __init__(self, stream, color):
        StreamWriter.__init__(self, stream)
        self.code = ANSI_CODES[color]
        self.reset = ANSI_CODES['reset']

    def write(self, s):
        StreamWriter.write(self, self.code)
        StreamWriter.write(self, s)
        StreamWriter.write(self, self.reset)

    def get_bgcolor(self):
        return 'unknown'


class WindowsColorBaseWriter(StreamWriter):
    """
    All Windows writers set the color without writing special control
    characters, so this class is convenient.
    """
    __module__ = __name__
    FOREGROUND_BLUE = 1
    FOREGROUND_GREEN = 2
    FOREGROUND_RED = 4
    FOREGROUND_INTENSITY = 8
    BACKGROUND_BLUE = 16
    BACKGROUND_GREEN = 32
    BACKGROUND_RED = 64
    BACKGROUND_INTENSITY = 128

    def __init__(self, stream, color):
        StreamWriter.__init__(self, stream)
        self.reset = self._get_color()
        self.background = self.reset & 240
        CODES = {'red': self.FOREGROUND_RED | self.FOREGROUND_INTENSITY | self.background, 'green': self.FOREGROUND_GREEN | self.FOREGROUND_INTENSITY | self.background, 'yellow': self.FOREGROUND_GREEN | self.FOREGROUND_RED | self.FOREGROUND_INTENSITY | self.background, 'blue': self.FOREGROUND_BLUE | self.FOREGROUND_INTENSITY | self.background}
        self.code = CODES[color]

    def write(self, s):
        self._set_color(self.code)
        StreamWriter.write(self, s)
        self._set_color(self.reset)

    def get_bgcolor(self):
        WHITE = self.BACKGROUND_RED | self.BACKGROUND_GREEN | self.BACKGROUND_BLUE | self.BACKGROUND_INTENSITY
        YELLOW = self.BACKGROUND_RED | self.BACKGROUND_GREEN | self.BACKGROUND_INTENSITY
        if self.background in [WHITE, YELLOW]:
            return 'light'
        else:
            return 'dark'


class Win32ColorWriterWithExecutable(WindowsColorBaseWriter):
    __module__ = __name__
    setcolor_path = os.path.join(sys.prefix, 'testoob', 'setcolor.exe')
    setcolor_available = os.path.isfile(setcolor_path)
    if not setcolor_available:
        setcolor_path = os.path.join('other', 'setcolor.exe')
        setcolor_available = os.path.isfile(setcolor_path)

    def _set_color(self, code):
        if self.setcolor_available:
            try:
                import subprocess
            except ImportError:
                from testoob.compatibility import subprocess
            else:
                subprocess.Popen('"%s" set %d' % (self.setcolor_path, code)).wait()

    def _get_color(self):
        if self.setcolor_available:
            try:
                import subprocess
            except ImportError:
                from testoob.compatibility import subprocess
            else:
                get_pipe = subprocess.Popen('"%s" get' % self.setcolor_path, stdout=subprocess.PIPE)
                (color_code, _) = get_pipe.communicate()
                return int(color_code)
        else:
            return 15


class Win32ConsoleColorWriter(WindowsColorBaseWriter):
    __module__ = __name__

    def _out_handle(self):
        import win32console
        return win32console.GetStdHandle(win32console.STD_OUTPUT_HANDLE)

    out_handle = property(_out_handle)

    def _set_color(self, code):
        self.out_handle.SetConsoleTextAttribute(code)

    def _get_color(self):
        return self.out_handle.GetConsoleScreenBufferInfo()['Attributes']


class WindowsCtypesColorWriter(WindowsColorBaseWriter):
    __module__ = __name__
    STD_OUTPUT_HANDLE = -11

    def _out_handle(self):
        import ctypes
        return ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)

    out_handle = property(_out_handle)

    def _console_screen_buffer_info(self):
        import ctypes, struct
        csbi = ctypes.create_string_buffer(22)
        res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(self.out_handle, csbi)
        assert res
        (bufx, bufy, curx, cury, wattr, left, top, right, bottom, maxx, maxy) = struct.unpack('hhhhHhhhhhh', csbi.raw)
        return {'bufx': bufx, 'bufy': bufy, 'curx': curx, 'cury': cury, 'wattr': wattr, 'left': left, 'top': top, 'right': right, 'bottom': bottom, 'maxx': maxx, 'maxy': maxy}

    console_screen_buffer_info = property(_console_screen_buffer_info)

    def _set_color(self, code):
        import ctypes
        ctypes.windll.kernel32.SetConsoleTextAttribute(self.out_handle, code)

    def _get_color(self):
        return self.console_screen_buffer_info['wattr']


def color_writers_creator(writer_class):

    class ColorWriters:
        __module__ = __name__

        def _get_warning_color(self, bgcolor):
            import options
            if options.bgcolor != 'auto':
                bgcolor = options.bgcolor
            bg_mapping = {'dark': 'yellow', 'light': 'blue', 'unknown': 'yellow'}
            warning_color = bg_mapping[bgcolor]
            return warning_color

        def __init__(self, stream):
            self.normal = StreamWriter(stream)
            self.success = writer_class(stream, 'green')
            self.failure = writer_class(stream, 'red')
            bgcolor = self.success.get_bgcolor()
            self.warning = writer_class(stream, self._get_warning_color(bgcolor))

    return ColorWriters


from textstream import TextStreamReporter

def create_colored_reporter(writer_class):

    class ColoredReporter(TextStreamReporter):
        __module__ = __name__

        def __init__(self, *args, **kwargs):
            kwargs['create_writers'] = color_writers_creator(writer_class)
            TextStreamReporter.__init__(self, *args, **kwargs)

    return ColoredReporter


def choose_color_writer():
    if 'TESTOOB_COLOR_WRITER' in os.environ:
        return eval(os.environ['TESTOOB_COLOR_WRITER'])
    if sys.platform != 'win32':
        return TerminalColorWriter
    try:
        import win32console
        return Win32ConsoleColorWriter
    except ImportError:
        pass

    try:
        import ctypes
        return WindowsCtypesColorWriter
    except ImportError:
        pass

    return Win32ColorWriterWithExecutable


ColoredTextReporter = create_colored_reporter(choose_color_writer())