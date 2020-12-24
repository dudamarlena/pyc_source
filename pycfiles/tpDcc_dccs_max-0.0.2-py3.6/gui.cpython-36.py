# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/dccs/max/core/gui.py
# Compiled at: 2020-04-11 22:25:56
# Size of source mod 2**32: 3265 bytes
from __future__ import print_function, division, absolute_import
from Qt.QtWidgets import *
import MaxPlus
from tpDcc.libs.python import path
from tpDcc.libs.qt.core import qtutils
from tpDcc.dccs.max.core import helpers

def get_max_window():
    """
    Returns an instance of the current Max window
    """
    version = int(helpers.get_max_version(as_year=True))
    if version == 2014:
        import ctypes, ctypes.wintypes
        pyobject = MaxPlus.Win32.GetMAXHWnd()
        hwndptr = pyobject.__int__()
        ptr = ctypes.c_void_p(hwndptr)
        ptrvalue = ptr.value
        clonglong = ctypes.c_longlong.from_address(ptrvalue)
        longhwnd = clonglong.value
        chwnd = ctypes.wintypes.HWND.from_address(ptrvalue)
        hwnd = clonglong.value
        return hwnd
    if version == 2015 or version == 2016:
        return long(MaxPlus.Win32.GetMAXHWnd())
    else:
        if version == 2017:
            return MaxPlus.GetQMaxWindow()
        return MaxPlus.GetQMaxMainWindow()


def to_qt_object(max_ptr, qobj=None):
    """
    Returns an instance of the Max UI element as a QWidget
    """
    if qtutils.QT_AVAILABLE:
        if not qobj:
            qobj = QWidget
        if max_ptr is not None:
            return qtutils.wrapinstance(long(max_ptr), qobj)


def open_get_path_dialog(init_directory=None):
    """
    Opens standard 3ds Max get path dialog
    :param init_directory: str, init directory to browse
    :return: str
    """
    result = MaxPlus.FPValue()
    if init_directory is None:
        MaxPlus.Core.EvalMAXScript('getSavePath caption:"Export directory" initialDir:(getDir #maxroot)', result)
    else:
        MaxPlus.Core.EvalMAXScript('getSavePath caption:"Export directory" initialDir:"{}"'.format(path.clean_path(init_directory)), result)
    try:
        selected_path = result.Get()
        return selected_path
    except Exception:
        return ''


def show_error_window(title, message):
    """
    Shows a native Max error window with the given title and message
    :param title: str, title of the error window
    :param message: str, message of the error window
    """
    message = message.replace('"', '\\"')
    cmd = 'messageBox "{}" title:"{}" beep:False'.format(message, title)
    MaxPlus.Core.EvalMAXScript(cmd)


def show_warning_message(message):
    """
    Prints a warning message in the 3ds Max listener window
    :param message: str, message of the warning
    """
    message = message.replace('"', '\\"')
    cmd = ''.join(('print "', message, '"'))
    MaxPlus.Core.EvalMAXScript(cmd)