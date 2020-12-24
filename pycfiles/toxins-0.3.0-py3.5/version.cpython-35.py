# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toxins/version.py
# Compiled at: 2016-12-18 09:58:01
# Size of source mod 2**32: 1148 bytes
"""
Project version:

>>> print(VERSION_INFO)
VersionInfo(major=0, minor=3, patch=0)
>>> print(VERSION)
0.3.0
>>>

"""
import collections
__author__ = 'Simone Campagna'
__copyright__ = 'Copyright (c) 2016 Simone Campagna'
__license__ = 'Apache License Version 2.0'
__all__ = ('VersionInfo', 'VERSION_INFO', 'VERSION')
VersionInfo = collections.namedtuple('VersionInfo', ('major', 'minor', 'patch'))
VERSION_INFO = VersionInfo(major=0, minor=3, patch=0)
VERSION = '.'.join(str(v) for v in VERSION_INFO)