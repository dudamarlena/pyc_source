# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/kgb/__init__.py
# Compiled at: 2020-04-10 23:22:42
from __future__ import unicode_literals
from kgb.agency import SpyAgency
from kgb.contextmanagers import spy_on
VERSION = (
 5, 0, 0, b'final', 0, True)

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
__all__ = [
 b'__version__',
 b'__version_info__',
 b'SpyAgency',
 b'VERSION',
 b'get_package_version',
 b'get_version_string',
 b'is_release',
 b'spy_on']