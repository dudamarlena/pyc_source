# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/package/release.py
# Compiled at: 2019-04-29 12:25:50
# Size of source mod 2**32: 610 bytes
"""Release information."""
from collections import namedtuple
version_info = namedtuple('version_info', ('major', 'minor', 'micro', 'releaselevel',
                                           'serial'))(2, 0, 1, 'final', 1)
version = '.'.join([str(i) for i in version_info[:3]]) + (version_info.releaselevel[0] + str(version_info.serial) if version_info.releaselevel != 'final' else '')
author = namedtuple('Author', ['name', 'email'])('Alice Bevan-McGregor', 'alice@gothcandy.com')
description = 'A collection of utilities for resolving object names, names to objects, and managing plugins/extensions.'
url = 'https://github.com/marrow/package/'