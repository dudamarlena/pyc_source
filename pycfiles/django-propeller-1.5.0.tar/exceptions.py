# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thorsten/code/django-propeller/django_propeller/exceptions.py
# Compiled at: 2017-03-24 13:36:01
from __future__ import unicode_literals

class PropellerException(Exception):
    """Any exception from this package"""
    pass


class PropellerError(PropellerException):
    """Any exception that is an error"""
    pass