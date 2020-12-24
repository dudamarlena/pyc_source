# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eugene/Workspace/django-rest-framework-registration/rest_framework_registration/signals.py
# Compiled at: 2016-04-01 05:29:03
# Size of source mod 2**32: 159 bytes
from django.dispatch import Signal
user_registered = Signal(providing_args=['user', 'request'])
user_activated = Signal(providing_args=['user', 'request'])