# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pn36swhz/pip/pip/_internal/utils/glibc.py
# Compiled at: 2020-02-14 17:24:54
# Size of source mod 2**32: 3297 bytes
from __future__ import absolute_import
import os, sys
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Optional, Tuple

def glibc_version_string():
    """Returns glibc version string, or None if not using glibc."""
    return glibc_version_string_confstr() or glibc_version_string_ctypes()


def glibc_version_string_confstr():
    """Primary implementation of glibc_version_string using os.confstr."""
    if sys.platform == 'win32':
        return
    try:
        _, version = os.confstr('CS_GNU_LIBC_VERSION').split()
    except (AttributeError, OSError, ValueError):
        return
    else:
        return version


def glibc_version_string_ctypes():
    """Fallback implementation of glibc_version_string using ctypes."""
    try:
        import ctypes
    except ImportError:
        return
    else:
        process_namespace = ctypes.CDLL(None)
        try:
            gnu_get_libc_version = process_namespace.gnu_get_libc_version
        except AttributeError:
            return
        else:
            gnu_get_libc_version.restype = ctypes.c_char_p
            version_str = gnu_get_libc_version()
            if not isinstance(version_str, str):
                version_str = version_str.decode('ascii')
            return version_str


def libc_ver():
    """Try to determine the glibc version

    Returns a tuple of strings (lib, version) which default to empty strings
    in case the lookup fails.
    """
    glibc_version = glibc_version_string()
    if glibc_version is None:
        return ('', '')
    return ('glibc', glibc_version)