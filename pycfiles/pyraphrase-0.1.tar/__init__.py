# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/mareike/work/app/pyrap-dev/_version/__init__.py
# Compiled at: 2018-01-31 08:50:30
__doc__ = '\n_version\nVersion information for pracmln.\n'
import sys
__all__ = [
 'VERSION_MAJOR',
 'VERSION_MINOR',
 'VERSION_PATCH',
 'VERSION_STRING',
 '__version__',
 '__basedir__']
VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = 0
VERSION_STRING_FULL = '%s.%s.%s' % (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)
VERSION_STRING_SHORT = '%s.%s' % (VERSION_MAJOR, VERSION_MINOR)
__version__ = VERSION_STRING_FULL
if sys.version_info[0] == 2:
    __basedir__ = 'python2'
elif sys.version_info[0] == 3:
    __basedir__ = 'python3'
else:
    raise Exception('Unsupported Python version: %s' % sys.version_info[0])