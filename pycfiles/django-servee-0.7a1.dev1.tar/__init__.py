# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: servee/__init__.py
# Compiled at: 2012-09-09 14:37:07
VERSION = (0, 7, 0, 'a', 1)
DEV_N = 1

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3] != 'f':
        version = '%s%s%s' % (version, VERSION[3], VERSION[4])
        if DEV_N:
            version = '%s.dev%s' % (version, DEV_N)
    return version


__version__ = get_version()