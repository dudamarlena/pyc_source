# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aedir_pproc/__about__.py
# Compiled at: 2020-04-01 10:59:06
# Size of source mod 2**32: 613 bytes
__doc__ = '\naedir_pproc.__about__ - Meta information\n'
import collections
VersionInfo = collections.namedtuple('version_info', ('major', 'minor', 'micro'))
__version_info__ = VersionInfo(major=1,
  minor=0,
  micro=1)
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