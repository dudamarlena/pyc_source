# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jishaku/meta.py
# Compiled at: 2020-03-05 23:53:06
# Size of source mod 2**32: 816 bytes
"""
jishaku.meta
~~~~~~~~~~~~

Meta information about jishaku.

:copyright: (c) 2020 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""
from collections import namedtuple
__all__ = ('__author__', '__copyright__', '__docformat__', '__license__', '__title__',
           '__version__', 'version_info')
VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
version_info = VersionInfo(major=1, minor=18, micro=2, releaselevel='final', serial=0)
__author__ = 'Gorialis'
__copyright__ = 'Copyright 2020 Devon (Gorialis) R'
__docformat__ = 'restructuredtext en'
__license__ = 'MIT'
__title__ = 'jishaku'
__version__ = '.'.join(map(str, (version_info.major, version_info.minor, version_info.micro)))