# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thorsten/code/django-propeller/django_propeller/exceptions.py
# Compiled at: 2017-02-17 14:40:23
# Size of source mod 2**32: 268 bytes
from __future__ import unicode_literals

class PropellerException(Exception):
    __doc__ = '\n    Any exception from this package\n    '


class PropellerError(PropellerException):
    __doc__ = '\n    Any exception that is an error\n    '