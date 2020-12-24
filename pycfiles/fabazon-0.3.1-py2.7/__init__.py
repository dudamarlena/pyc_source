# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/fabazon/__init__.py
# Compiled at: 2019-04-05 04:41:22
VERSION = (
 0, 3, 1, 'final', 0, True)

def get_version_string():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version += '.%s' % VERSION[2]
    if VERSION[3] != 'final':
        if VERSION[3] == 'rc':
            version += ' RC%s' % VERSION[4]
        else:
            version += ' %s %s' % (VERSION[3], VERSION[4])
    if not is_release():
        version += ' (dev)'
    return version


def get_package_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version += '.%s' % VERSION[2]
    if VERSION[3] != 'final':
        version += '%s%s' % (VERSION[3], VERSION[4])
    return version


def is_release():
    return VERSION[5]


__version_info__ = VERSION[:-1]
__version__ = get_package_version()