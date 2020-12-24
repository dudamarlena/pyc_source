# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\audit\signals.py
# Compiled at: 2010-04-29 12:25:29
from django.dispatch import Signal
audit_special = Signal(providing_args=['instance', 'field', 'action', 'value'])