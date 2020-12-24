# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Development\django2-propeller\django2_propeller\exceptions.py
# Compiled at: 2019-04-26 08:32:14
# Size of source mod 2**32: 268 bytes
from __future__ import unicode_literals

class PropellerException(Exception):
    __doc__ = 'Any exception from this package'


class PropellerError(PropellerException):
    __doc__ = 'Any exception that is an error'