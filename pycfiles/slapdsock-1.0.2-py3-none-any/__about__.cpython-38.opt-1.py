# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /slapdsock/__about__.py
# Compiled at: 2020-05-13 07:59:56
# Size of source mod 2**32: 904 bytes
"""
slapdsock.__about__ - Meta information

slapdsock - OpenLDAP back-sock listeners with Python
see https://www.stroeder.com/slapdsock.html

(c) 2015-2020 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import collections
VersionInfo = collections.namedtuple('version_info', ('major', 'minor', 'micro'))
__version_info__ = VersionInfo(major=1,
  minor=0,
  micro=2)
__version__ = '.'.join((str(val) for val in __version_info__))
__author__ = 'Michael Stroeder'
__mail__ = 'michael@stroeder.com'
__copyright__ = '(C) 2015-2020 by Michael Ströder <michael@stroeder.com>'
__license__ = 'Apache-2.0'
__all__ = [
 '__version_info__',
 '__version__',
 '__author__',
 '__mail__',
 '__license__',
 '__copyright__']