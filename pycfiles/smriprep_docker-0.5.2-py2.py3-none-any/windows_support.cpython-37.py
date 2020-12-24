# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pn36swhz/setuptools/setuptools/windows_support.py
# Compiled at: 2020-02-14 17:24:53
# Size of source mod 2**32: 714 bytes
import platform, ctypes

def windows_only(func):
    if platform.system() != 'Windows':
        return lambda *args, **kwargs: None
    return func


@windows_only
def hide_file(path):
    """
    Set the hidden attribute on a file or directory.

    From http://stackoverflow.com/questions/19622133/

    `path` must be text.
    """
    __import__('ctypes.wintypes')
    SetFileAttributes = ctypes.windll.kernel32.SetFileAttributesW
    SetFileAttributes.argtypes = (ctypes.wintypes.LPWSTR, ctypes.wintypes.DWORD)
    SetFileAttributes.restype = ctypes.wintypes.BOOL
    FILE_ATTRIBUTE_HIDDEN = 2
    ret = SetFileAttributes(path, FILE_ATTRIBUTE_HIDDEN)
    if not ret:
        raise ctypes.WinError()