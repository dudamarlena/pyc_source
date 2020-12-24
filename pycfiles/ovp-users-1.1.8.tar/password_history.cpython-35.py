# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/models/password_history.py
# Compiled at: 2017-05-22 20:56:40
# Size of source mod 2**32: 241 bytes
from django.db import models

class PasswordHistory(models.Model):
    hashed_password = models.CharField(max_length=300)
    user = models.ForeignKey('ovp_users.User')
    set_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)