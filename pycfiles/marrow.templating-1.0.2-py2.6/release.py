# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/marrow/templating/release.py
# Compiled at: 2012-05-23 13:18:32
"""Release information about marrow.templating."""
from collections import namedtuple
__all__ = [
 'version_info', 'version', 'copyright']
version_info = namedtuple('version_info', ('major', 'minor', 'micro', 'releaselevel',
                                           'serial'))(1, 0, 2, 'final', 1)
version = ('.').join([ str(i) for i in version_info[:3] ]) + (version_info.releaselevel[0] + str(version_info.serial) if version_info.releaselevel != 'final' else '')
copyright = '2009-2012, Alice Bevan-McGregor and contributors'