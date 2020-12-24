# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/virtualenv_multiver/__init__.py
# Compiled at: 2015-06-28 04:47:09
from __future__ import unicode_literals
VERSION = (
 0, 5, 0, b'final', 0, True)

def get_version_string():
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
    version = b'%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version += b'.%s' % VERSION[2]
    if VERSION[3] != b'final':
        version += b'%s%s' % (VERSION[3], VERSION[4])
    return version


def is_release():
    return VERSION[5]


__version_info__ = VERSION[:-1]
__version__ = get_package_version()