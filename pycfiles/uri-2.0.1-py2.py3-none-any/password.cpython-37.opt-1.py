# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /uri/part/password.py
# Compiled at: 2018-10-22 09:58:17
# Size of source mod 2**32: 160 bytes
from __future__ import unicode_literals
from .base import ProxyPart

class PasswordPart(ProxyPart):
    attribute = '_password'
    prefix = ':'