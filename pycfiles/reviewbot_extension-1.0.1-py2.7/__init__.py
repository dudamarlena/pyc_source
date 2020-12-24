# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbotext/__init__.py
# Compiled at: 2018-07-31 04:09:55
from __future__ import unicode_literals
VERSION = (
 1, 0, 1, b'final', 0, True)

def get_version_string():
    """Return the version of Review Bot.

    Returns:
        unicode:
        The full version.
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
    """Return the package version of Review Bot.

    This is a simplified version string which is used when building a package.

    Returns:
        unicode:
        The version to use for the package.
    """
    version = b'%d.%d' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version += b'.%d' % VERSION[2]
    if VERSION[3] != b'final':
        version += b'%s%d' % (VERSION[3], VERSION[4])
    return version


def is_release():
    """Return whether the current version is a release.

    Returns:
        boolean:
        True if the current version of Review Bot is a released package.
    """
    return VERSION[5]


__version_info__ = VERSION[:-1]
__version__ = get_package_version()