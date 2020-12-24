# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/marrow/util/release.py
# Compiled at: 2012-10-11 17:41:43
"""Release information about Marrow Interface."""
from collections import namedtuple
__all__ = [
 'version_info', 'version']
version_info = namedtuple('version_info', ('major', 'minor', 'micro', 'releaselevel',
                                           'serial'))(1, 2, 3, 'final', 0)
version = ('.').join([ str(i) for i in version_info[:3] ]) + (version_info.releaselevel[0] + str(version_info.serial) if version_info.releaselevel != 'final' else '')