# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/GitHub/django_sendgrid_repo/django_sendgrid_parse/admin.py
# Compiled at: 2016-08-21 23:09:38
# Size of source mod 2**32: 129 bytes
from django.contrib import admin
from . import models
admin.site.register(models.Attachment)
admin.site.register(models.Email)