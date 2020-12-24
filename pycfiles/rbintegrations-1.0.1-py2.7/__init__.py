# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/d6/k73lbsvs0fl4s0r7l3nh67wr0000gn/T/beanbag-tools.RLX_st/rbintegrations/__init__.py
# Compiled at: 2020-01-07 04:31:42
"""RBIntegrations version and package information.

These variables and functions can be used to identify the version of
the module. They're largely used for packaging purposes.
"""
from __future__ import unicode_literals
VERSION = (
 1, 0, 1, 0, b'final', 0, True)

def get_version_string():
    """Return the version as a human-readable string.

    Returns:
        unicode:
        The human-readable version.
    """
    version = b'%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2] or VERSION[3]:
        version += b'.%s' % VERSION[2]
    if VERSION[3]:
        version += b'.%s' % VERSION[3]
    if VERSION[4] != b'final':
        if VERSION[4] == b'rc':
            version += b' RC%s' % VERSION[5]
        else:
            version += b' %s %s' % (VERSION[4], VERSION[5])
    if not is_release():
        version += b' (dev)'
    return version


def get_package_version():
    """Return the version as a Python package version string.

    Returns:
        unicode:
        The package version.
    """
    version = b'%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2] or VERSION[3]:
        version += b'.%s' % VERSION[2]
    if VERSION[3]:
        version += b'.%s' % VERSION[3]
    if VERSION[4] != b'final':
        version += b'%s%s' % (VERSION[4], VERSION[5])
    return version


def is_release():
    """Return whether this is a released version.

    Returns:
        bool:
        ``True`` if this is a released version, or ``False`` if it's still
        in development.
    """
    return VERSION[6]


__version_info__ = VERSION[:-1]
__version__ = get_package_version()