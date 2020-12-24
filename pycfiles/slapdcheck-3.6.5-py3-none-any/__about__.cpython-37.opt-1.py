# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /slapdcheck/__about__.py
# Compiled at: 2020-02-20 07:49:30
# Size of source mod 2**32: 611 bytes
"""
slapdcheck.__about__ - Meta information
"""
import collections
VersionInfo = collections.namedtuple('version_info', ('major', 'minor', 'micro'))
__version_info__ = VersionInfo(major=3,
  minor=6,
  micro=5)
__version__ = '.'.join((str(val) for val in __version_info__))
__author__ = 'Michael Stroeder'
__mail__ = 'michael@stroeder.com'
__copyright__ = '(C) 2016-2020 by Michael Ströder <michael@stroeder.com>'
__license__ = 'Apache-2.0'
__all__ = [
 '__version_info__',
 '__version__',
 '__author__',
 '__mail__',
 '__license__',
 '__copyright__']