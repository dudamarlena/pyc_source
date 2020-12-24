# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/util/colorama/win32.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 4901 bytes
STDOUT = -11
STDERR = -12
try:
    from ctypes import windll
    from ctypes import wintypes
except ImportError:
    windll = None
    SetConsoleTextAttribute = lambda *_: None
else:
    from ctypes import byref, Structure, c_char, c_short, c_int, c_uint32, c_ushort, c_void_p, POINTER

    class CONSOLE_SCREEN_BUFFER_INFO(Structure):
        __doc__ = 'struct in wincon.h.'
        _fields_ = [
         (
          'dwSize', wintypes._COORD),
         (
          'dwCursorPosition', wintypes._COORD),
         (
          'wAttributes', wintypes.WORD),
         (
          'srWindow', wintypes.SMALL_RECT),
         (
          'dwMaximumWindowSize', wintypes._COORD)]

        def __str__(self):
            return '(%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)' % (
             self.dwSize.Y, self.dwSize.X,
             self.dwCursorPosition.Y, self.dwCursorPosition.X,
             self.wAttributes,
             self.srWindow.Top, self.srWindow.Left, self.srWindow.Bottom, self.srWindow.Right,
             self.dwMaximumWindowSize.Y, self.dwMaximumWindowSize.X)


    _GetStdHandle = windll.kernel32.GetStdHandle
    _GetStdHandle.argtypes = [
     wintypes.DWORD]
    _GetStdHandle.restype = wintypes.HANDLE
    _GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo
    _GetConsoleScreenBufferInfo.argtypes = [
     wintypes.HANDLE,
     c_void_p]
    _GetConsoleScreenBufferInfo.restype = wintypes.BOOL
    _SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
    _SetConsoleTextAttribute.argtypes = [
     wintypes.HANDLE,
     wintypes.WORD]
    _SetConsoleTextAttribute.restype = wintypes.BOOL
    _SetConsoleCursorPosition = windll.kernel32.SetConsoleCursorPosition
    _SetConsoleCursorPosition.argtypes = [
     wintypes.HANDLE,
     c_int]
    _SetConsoleCursorPosition.restype = wintypes.BOOL
    _FillConsoleOutputCharacterA = windll.kernel32.FillConsoleOutputCharacterA
    _FillConsoleOutputCharacterA.argtypes = [
     wintypes.HANDLE,
     c_char,
     wintypes.DWORD,
     wintypes._COORD,
     POINTER(wintypes.DWORD)]
    _FillConsoleOutputCharacterA.restype = wintypes.BOOL
    _FillConsoleOutputAttribute = windll.kernel32.FillConsoleOutputAttribute
    _FillConsoleOutputAttribute.argtypes = [
     wintypes.HANDLE,
     wintypes.WORD,
     wintypes.DWORD,
     c_int,
     POINTER(wintypes.DWORD)]
    _FillConsoleOutputAttribute.restype = wintypes.BOOL
    handles = {STDOUT: _GetStdHandle(STDOUT), 
     STDERR: _GetStdHandle(STDERR)}

    def GetConsoleScreenBufferInfo(stream_id=STDOUT):
        handle = handles[stream_id]
        csbi = CONSOLE_SCREEN_BUFFER_INFO()
        success = _GetConsoleScreenBufferInfo(handle, byref(csbi))
        return csbi


    def SetConsoleTextAttribute(stream_id, attrs):
        handle = handles[stream_id]
        return _SetConsoleTextAttribute(handle, attrs)


    def SetConsoleCursorPosition(stream_id, position):
        position = (wintypes._COORD)(*position)
        if position.Y <= 0 or position.X <= 0:
            return
        adjusted_position = wintypes._COORD(position.Y - 1, position.X - 1)
        sr = GetConsoleScreenBufferInfo(STDOUT).srWindow
        adjusted_position.Y += sr.Top
        adjusted_position.X += sr.Left
        handle = handles[stream_id]
        return _SetConsoleCursorPosition(handle, adjusted_position)


    def FillConsoleOutputCharacter(stream_id, char, length, start):
        handle = handles[stream_id]
        char = c_char(char)
        length = wintypes.DWORD(length)
        num_written = wintypes.DWORD(0)
        success = _FillConsoleOutputCharacterA(handle, char, length, start, byref(num_written))
        return num_written.value


    def FillConsoleOutputAttribute(stream_id, attr, length, start):
        """ FillConsoleOutputAttribute( hConsole, csbi.wAttributes, dwConSize, coordScreen, &cCharsWritten )"""
        handle = handles[stream_id]
        attribute = wintypes.WORD(attr)
        length = wintypes.DWORD(length)
        num_written = wintypes.DWORD(0)
        return _FillConsoleOutputAttribute(handle, attribute, length, start, byref(num_written))