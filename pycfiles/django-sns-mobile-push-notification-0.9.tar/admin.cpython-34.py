# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rvaziri/django_mobile_push/sns_mobile_push_notification/admin.py
# Compiled at: 2018-04-29 13:22:49
# Size of source mod 2**32: 148 bytes
from django.contrib import admin
from sns_mobile_push_notification.models import Device, Log
admin.site.register(Device)
admin.site.register(Log)