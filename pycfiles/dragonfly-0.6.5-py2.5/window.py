# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\windows\window.py
# Compiled at: 2009-03-09 13:06:57
"""
    This file implements a Window class as an interface to the Win32
    window control and placement.
"""
import win32gui, win32con
from ctypes import windll, pointer, c_wchar, c_ulong
from .rectangle import Rectangle, unit
from .monitor import monitors

class Window(object):
    _windows_by_name = {}
    _windows_by_handle = {}

    @classmethod
    def get_foreground(cls):
        handle = win32gui.GetForegroundWindow()
        if handle in cls._windows_by_handle:
            return cls._windows_by_handle[handle]
        window = Window(handle=handle)
        return window

    @classmethod
    def get_all_windows(cls):

        def function(handle, argument):
            argument.append(Window(handle))

        argument = []
        win32gui.EnumWindows(function, argument)
        return argument

    def __init__(self, handle):
        self._handle = None
        self._names = set()
        self.handle = handle
        return

    def __str__(self):
        args = ['handle=%d' % self._handle] + list(self._names)
        return '%s(%s)' % (self.__class__.__name__, (', ').join(args))

    def _set_handle(self, handle):
        assert isinstance(handle, int)
        self._handle = handle
        self._windows_by_handle[handle] = self

    handle = property(fget=lambda self: self._handle, fset=_set_handle, doc='Protected access to handle attribute.')

    def _get_name(self):
        if not self._names:
            return
        for name in self._names:
            return name

        return

    def _set_name(self, name):
        assert isinstance(name, basestring)
        self._names.add(name)
        self._windows_by_name[name] = self

    name = property(fget=_get_name, fset=_set_name, doc='Protected access to name attribute.')

    def _win32gui_func(name):
        func = getattr(win32gui, name)
        return lambda self: func(self._handle)

    _get_rect = _win32gui_func('GetWindowRect')
    _destroy = _win32gui_func('DestroyWindow')
    _set_foreground = _win32gui_func('SetForegroundWindow')
    _bring_to_top = _win32gui_func('BringWindowToTop')
    _get_window_text = _win32gui_func('GetWindowText')
    _get_class_name = _win32gui_func('GetClassName')
    title = property(fget=_get_window_text)
    classname = property(fget=_get_class_name)

    def _win32gui_test(name):
        test = getattr(win32gui, name)
        fget = lambda self: test(self._handle) and True or False
        return property(fget=fget, doc='Shortcut to win32gui.%s() function.' % name)

    is_valid = _win32gui_test('IsWindow')
    is_enabled = _win32gui_test('IsWindowEnabled')
    is_visible = _win32gui_test('IsWindowVisible')
    is_minimized = _win32gui_test('IsIconic')

    def _win32gui_show_window(state):
        return lambda self: win32gui.ShowWindow(self._handle, state)

    minimize = _win32gui_show_window(win32con.SW_MINIMIZE)
    maximize = _win32gui_show_window(win32con.SW_MAXIMIZE)
    restore = _win32gui_show_window(win32con.SW_RESTORE)

    def _get_window_module(self):
        pid = c_ulong()
        windll.user32.GetWindowThreadProcessId(self._handle, pointer(pid))
        handle = windll.kernel32.OpenProcess(1040, 0, pid)
        buf_len = 256
        buf = (c_wchar * buf_len)()
        windll.psapi.GetModuleFileNameExW(handle, 0, pointer(buf), buf_len)
        buf = buf[:]
        buf = buf[:buf.index('\x00')]
        return str(buf)

    executable = property(fget=_get_window_module)

    def get_position(self):
        (l, t, r, b) = self._get_rect()
        w = r - l
        h = b - t
        return Rectangle(l, t, w, h)

    def set_position(self, rectangle):
        assert isinstance(rectangle, Rectangle)
        (l, t, w, h) = rectangle.ltwh
        win32gui.MoveWindow(self._handle, l, t, w, h, 1)

    def get_containing_monitor(self):
        center = self.get_position().center
        for monitor in monitors:
            if monitor.rectangle.contains(center):
                return monitor

        return monitors[0]

    def get_normalized_position(self):
        monitor = self.get_containing_monitor()
        rectangle = self.get_position()
        rectangle.renormalize(monitor.rectangle, unit)
        return rectangle

    def set_normalized_position(self, rectangle, monitor=None):
        if not monitor:
            monitor = self.get_containing_monitor()
        rectangle.renormalize(unit, monitor.rectangle)
        self.set_position(rectangle)

    def set_foreground(self):
        if self.is_minimized:
            self.restore()
        self._set_foreground()