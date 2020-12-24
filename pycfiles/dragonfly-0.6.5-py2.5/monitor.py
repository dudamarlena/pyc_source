# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\windows\monitor.py
# Compiled at: 2009-03-12 04:21:42
"""
    This file offers an interface to the Win32 information about
    available monitors (a.k.a. screens, displays).
"""
import win32gui, ctypes
from ..log import get_log
from .rectangle import Rectangle
monitors = []

class Monitor(object):
    _log = get_log('monitor.init')

    def __init__(self, handle, rectangle):
        assert isinstance(handle, int)
        self._handle = handle
        assert isinstance(rectangle, Rectangle)
        self._rectangle = rectangle

    def __str__(self):
        return '%s(%d)' % (self.__class__.__name__, self._handle)

    def _set_handle(self, handle):
        assert isinstance(handle, int)
        self._handle = handle

    handle = property(fget=lambda self: self._handle, fset=_set_handle, doc='Protected access to handle attribute.')

    def _set_rectangle(self, rectangle):
        assert isinstance(rectangle, Rectangle)
        self._rectangle = rectangle

    rectangle = property(fget=lambda self: self._rectangle, fset=_set_rectangle, doc='Protected access to rectangle attribute.')


class _rect_t(ctypes.Structure):
    _fields_ = [
     (
      'left', ctypes.c_long),
     (
      'top', ctypes.c_long),
     (
      'right', ctypes.c_long),
     (
      'bottom', ctypes.c_long)]


class _monitor_info_t(ctypes.Structure):
    _fields_ = [
     (
      'cbSize', ctypes.c_ulong),
     (
      'rcMonitor', _rect_t),
     (
      'rcWork', _rect_t),
     (
      'dwFlags', ctypes.c_ulong)]


callback_t = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(_rect_t), ctypes.c_double)

def _callback(hMonitor, hdcMonitor, lprcMonitor, dwData):
    info = _monitor_info_t()
    info.cbSize = ctypes.sizeof(_monitor_info_t)
    info.rcMonitor = _rect_t()
    info.rcWork = _rect_t()
    res = ctypes.windll.user32.GetMonitorInfoA(hMonitor, ctypes.byref(info))
    handle = int(hMonitor)
    r = info.rcWork
    rectangle = Rectangle(r.left, r.top, r.right - r.left, r.bottom - r.top)
    monitor = Monitor(handle, rectangle)
    Monitor._log.debug('Found monitor %s with geometry %s.' % (
     monitor, rectangle))
    monitors.append(monitor)
    return True


res = ctypes.windll.user32.EnumDisplayMonitors(0, 0, callback_t(_callback), 0)