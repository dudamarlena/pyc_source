# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/thirdparty/colorama/win32.py
# Compiled at: 2013-12-09 06:41:17
STDOUT = -11
STDERR = -12
try:
    from ctypes import windll
except ImportError:
    windll = None
    SetConsoleTextAttribute = lambda *_: None
else:
    from ctypes import byref, Structure, c_char, c_short, c_uint32, c_ushort
    handles = {STDOUT: windll.kernel32.GetStdHandle(STDOUT), 
       STDERR: windll.kernel32.GetStdHandle(STDERR)}
    SHORT = c_short
    WORD = c_ushort
    DWORD = c_uint32
    TCHAR = c_char

    class COORD(Structure):
        """struct in wincon.h"""
        _fields_ = [
         (
          'X', SHORT),
         (
          'Y', SHORT)]


    class SMALL_RECT(Structure):
        """struct in wincon.h."""
        _fields_ = [
         (
          'Left', SHORT),
         (
          'Top', SHORT),
         (
          'Right', SHORT),
         (
          'Bottom', SHORT)]


    class CONSOLE_SCREEN_BUFFER_INFO(Structure):
        """struct in wincon.h."""
        _fields_ = [
         (
          'dwSize', COORD),
         (
          'dwCursorPosition', COORD),
         (
          'wAttributes', WORD),
         (
          'srWindow', SMALL_RECT),
         (
          'dwMaximumWindowSize', COORD)]

        def __str__(self):
            return '(%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)' % (
             self.dwSize.Y, self.dwSize.X,
             self.dwCursorPosition.Y, self.dwCursorPosition.X,
             self.wAttributes,
             self.srWindow.Top, self.srWindow.Left, self.srWindow.Bottom, self.srWindow.Right,
             self.dwMaximumWindowSize.Y, self.dwMaximumWindowSize.X)


    def GetConsoleScreenBufferInfo(stream_id=STDOUT):
        handle = handles[stream_id]
        csbi = CONSOLE_SCREEN_BUFFER_INFO()
        success = windll.kernel32.GetConsoleScreenBufferInfo(handle, byref(csbi))
        return csbi


    def SetConsoleTextAttribute(stream_id, attrs):
        handle = handles[stream_id]
        return windll.kernel32.SetConsoleTextAttribute(handle, attrs)


    def SetConsoleCursorPosition(stream_id, position):
        position = COORD(*position)
        if position.Y <= 0 or position.X <= 0:
            return
        adjusted_position = COORD(position.Y - 1, position.X - 1)
        sr = GetConsoleScreenBufferInfo(STDOUT).srWindow
        adjusted_position.Y += sr.Top
        adjusted_position.X += sr.Left
        handle = handles[stream_id]
        return windll.kernel32.SetConsoleCursorPosition(handle, adjusted_position)


    def FillConsoleOutputCharacter(stream_id, char, length, start):
        handle = handles[stream_id]
        char = TCHAR(char)
        length = DWORD(length)
        num_written = DWORD(0)
        success = windll.kernel32.FillConsoleOutputCharacterA(handle, char, length, start, byref(num_written))
        return num_written.value


    def FillConsoleOutputAttribute(stream_id, attr, length, start):
        """ FillConsoleOutputAttribute( hConsole, csbi.wAttributes, dwConSize, coordScreen, &cCharsWritten )"""
        handle = handles[stream_id]
        attribute = WORD(attr)
        length = DWORD(length)
        num_written = DWORD(0)
        return windll.kernel32.FillConsoleOutputAttribute(handle, attribute, length, start, byref(num_written))