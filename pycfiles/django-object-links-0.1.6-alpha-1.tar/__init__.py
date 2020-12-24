# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dstufft/django-object-links/object_links/__init__.py
# Compiled at: 2009-11-29 20:27:21
VERSION = (0, 1, 6, 'alpha', 1)
__version__ = ('.').join(map(str, VERSION))

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    elif VERSION[3] != 'final':
        version = '%s %s %s' % (version, VERSION[3], VERSION[4])
    return version