# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/key/signals.py
# Compiled at: 2011-11-17 12:47:53
from django.dispatch import Signal
api_user_created = Signal(providing_args=['instance'])
api_key_created = Signal(providing_args=['instance'])
api_user_logged_in = Signal(providing_args=['instance'])
api_user_logged_out = Signal(providing_args=['instance'])