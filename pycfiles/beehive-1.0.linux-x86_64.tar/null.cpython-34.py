# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/formatter/null.py
# Compiled at: 2014-10-30 08:03:31
# Size of source mod 2**32: 337 bytes
from beehive.formatter.base import Formatter

class NullFormatter(Formatter):
    __doc__ = '\n    Provides formatter that does not output anything.\n    Implements the NULL pattern for a formatter (similar like: /dev/null).\n    '
    name = 'null'
    description = 'Provides formatter that does not output anything.'