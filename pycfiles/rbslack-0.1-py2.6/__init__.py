# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/rbslack/__init__.py
# Compiled at: 2016-03-05 05:42:36
from __future__ import unicode_literals
VERSION = (
 0, 1, 0, 0, b'final', 0, True)

def get_version_string():
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
    version = b'%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2] or VERSION[3]:
        version += b'.%s' % VERSION[2]
    if VERSION[3]:
        version += b'.%s' % VERSION[3]
    if VERSION[4] != b'final':
        version += b'%s%s' % (VERSION[4], VERSION[5])
    return version


def is_release():
    return VERSION[6]


__version_info__ = VERSION[:-1]
__version__ = get_package_version()