# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/marrow/cache/release.py
# Compiled at: 2015-04-23 13:32:48
"""Release information about Marrow Cache."""
from collections import namedtuple
version_info = namedtuple('version_info', ('major', 'minor', 'micro', 'releaselevel',
                                           'serial'))(1, 0, 3, 'final', 1)
version = ('.').join([ str(i) for i in version_info[:3] ]) + (version_info.releaselevel[0] + str(version_info.serial) if version_info.releaselevel != 'final' else '')
author = namedtuple('Author', ['name', 'email'])('Alice Bevan-McGregor', 'alice@gothcandy.com')
description = 'An extension to MongoEngine for memoization and document-aware caching.'
url = 'https://github.com/marrow/cache/'