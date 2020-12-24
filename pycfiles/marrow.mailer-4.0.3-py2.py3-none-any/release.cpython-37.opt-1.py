# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mailer/release.py
# Compiled at: 2019-09-15 20:05:09
# Size of source mod 2**32: 630 bytes
"""Release information about Marrow Mailer."""
from collections import namedtuple
version_info = namedtuple('version_info', ('major', 'minor', 'micro', 'releaselevel',
                                           'serial'))(4, 0, 3, 'final', 0)
version = '.'.join([str(i) for i in version_info[:3]]) + (version_info.releaselevel[0] + str(version_info.serial) if version_info.releaselevel != 'final' else '')
author = namedtuple('Author', ['name', 'email'])('Alice Bevan-McGregor', 'alice@gothcandy.com')
description = 'A light-weight modular mail delivery framework for Python 2.7+, 3.3+, Pypy, and Pypy3.'
url = 'https://github.com/marrow/mailer/'