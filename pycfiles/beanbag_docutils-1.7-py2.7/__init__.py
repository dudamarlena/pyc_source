# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/beanbag_docutils/__init__.py
# Compiled at: 2018-06-14 23:50:40
from __future__ import unicode_literals
VERSION = (
 1, 7, 0, b'final', 0, True)

def get_version_string():
    """Return the version as a human-readable string.

    Returns:
        unicode:
        The version number as a human-readable string.
    """
    version = b'%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version += b'.%s' % VERSION[2]
    if VERSION[3] != b'final':
        if VERSION[3] == b'rc':
            version += b' RC%s' % VERSION[4]
        else:
            version += b' %s %s' % (VERSION[3], VERSION[4])
    if not is_release():
        version += b' (dev)'
    return version


def get_package_version():
    """Return the version as a Python package version string.

    Returns:
        unicode:
        The version number as used in a Python package.
    """
    version = b'%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version += b'.%s' % VERSION[2]
    if VERSION[3] != b'final':
        version += b'%s%s' % (VERSION[3], VERSION[4])
    return version


def is_release():
    """Return whether this is a released version.

    Returns:
        bool:
        ``True`` if this is a released version of the package.
    """
    return VERSION[5]


__version_info__ = VERSION[:-1]
__version__ = get_package_version()