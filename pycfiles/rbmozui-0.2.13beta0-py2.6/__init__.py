# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rbmozui/__init__.py
# Compiled at: 2015-02-13 18:59:44
VERSION = (
 0, 2, 13, 'beta', 0, False)

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
    version = '%d.%d' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version += '.%d' % VERSION[2]
    if VERSION[3] != 'final':
        version += '%s%d' % (VERSION[3], VERSION[4])
    return version


def is_release():
    return VERSION[5]


__version_info__ = VERSION[:-1]
__version__ = get_package_version()