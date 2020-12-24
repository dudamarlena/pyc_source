# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/release.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 659 bytes
"""Release information about Marrow Mongo."""
from __future__ import unicode_literals
from collections import namedtuple
version_info = namedtuple('version_info', ('major', 'minor', 'micro', 'releaselevel',
                                           'serial'))(1, 1, 2, 'final', 0)
version = '.'.join([str(i) for i in version_info[:3]]) + (version_info.releaselevel[0] + str(version_info.serial) if version_info.releaselevel != 'final' else '')
author = namedtuple('Author', ['name', 'email'])('Alice Bevan-McGregor', 'alice@gothcandy.com')
description = 'Light-weight utilities to augment, not replace the Python MongoDB driver.'
url = 'https://github.com/marrow/mongo/'