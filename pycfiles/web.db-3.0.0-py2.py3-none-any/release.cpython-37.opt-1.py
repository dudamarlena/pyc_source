# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/db/release.py
# Compiled at: 2019-06-09 23:25:11
# Size of source mod 2**32: 662 bytes
"""Release information about this WebCore add-on."""
from collections import namedtuple
version_info = namedtuple('version_info', ('major', 'minor', 'micro', 'releaselevel',
                                           'serial'))(3, 0, 0, 'final', 0)
version = '.'.join([str(i) for i in version_info[:3]]) + (version_info.releaselevel[0] + str(version_info.serial) if version_info.releaselevel != 'final' else '')
author = namedtuple('Author', ['name', 'email'])('Alice Bevan-McGregor', 'alice@gothcandy.com')
description = 'General database adapter layer for common configuration and operation.'
copyright = '2009-2019, Alice Bevan-McGregor and contributors'
url = 'https://github.com/marrow/web.db'