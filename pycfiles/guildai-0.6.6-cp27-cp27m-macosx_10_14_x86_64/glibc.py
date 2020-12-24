# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./guild/external/pip/_internal/utils/glibc.py
# Compiled at: 2019-09-10 15:18:29
from __future__ import absolute_import
import ctypes, re, warnings

def glibc_version_string():
    """Returns glibc version string, or None if not using glibc."""
    process_namespace = ctypes.CDLL(None)
    try:
        gnu_get_libc_version = process_namespace.gnu_get_libc_version
    except AttributeError:
        return

    gnu_get_libc_version.restype = ctypes.c_char_p
    version_str = gnu_get_libc_version()
    if not isinstance(version_str, str):
        version_str = version_str.decode('ascii')
    return version_str


def check_glibc_version(version_str, required_major, minimum_minor):
    m = re.match('(?P<major>[0-9]+)\\.(?P<minor>[0-9]+)', version_str)
    if not m:
        warnings.warn('Expected glibc version with 2 components major.minor, got: %s' % version_str, RuntimeWarning)
        return False
    return int(m.group('major')) == required_major and int(m.group('minor')) >= minimum_minor


def have_compatible_glibc(required_major, minimum_minor):
    version_str = glibc_version_string()
    if version_str is None:
        return False
    else:
        return check_glibc_version(version_str, required_major, minimum_minor)


def libc_ver():
    """Try to determine the glibc version

    Returns a tuple of strings (lib, version) which default to empty strings
    in case the lookup fails.
    """
    glibc_version = glibc_version_string()
    if glibc_version is None:
        return ('', '')
    else:
        return (
         'glibc', glibc_version)
        return