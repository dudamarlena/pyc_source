# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nyga/work/code/pracmln/python2/pracmln/_version/__init__.py
# Compiled at: 2018-04-24 04:48:32
"""
_version
Version information for pracmln.
"""
import sys
__all__ = [
 'VERSION_MAJOR',
 'VERSION_MINOR',
 'VERSION_PATCH',
 'VERSION_STRING',
 'APPNAME',
 'APPAUTHOR',
 '__version__',
 '__basedir__']
APPNAME = 'pracmln'
APPAUTHOR = 'danielnyga'
VERSION_MAJOR = 1
VERSION_MINOR = 2
VERSION_PATCH = 3
VERSION_STRING_FULL = '%s.%s.%s' % (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)
VERSION_STRING_SHORT = '%s.%s' % (VERSION_MAJOR, VERSION_MINOR)
__version__ = VERSION_STRING_FULL
if sys.version_info[0] == 2:
    __basedir__ = 'python2'
elif sys.version_info[0] == 3:
    __basedir__ = 'python3'
else:
    raise Exception('Unsupported Python version: %s' % sys.version_info[0])