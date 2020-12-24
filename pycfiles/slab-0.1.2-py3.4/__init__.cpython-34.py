# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slab/__init__.py
# Compiled at: 2016-01-08 05:50:10
# Size of source mod 2**32: 444 bytes
import collections
__author__ = 'Federico Ficarelli'
__copyright__ = 'Copyright (c) 2015 Federico Ficarelli'
__license__ = 'Apache License Version 2.0'
__all__ = ('VERSION_INFO', 'VERSION')
VersionInfo = collections.namedtuple('VersionInfo', ('major', 'minor', 'patch'))
VERSION_INFO = VersionInfo(major=0, minor=1, patch=2)
VERSION = '.'.join(str(v) for v in VERSION_INFO)