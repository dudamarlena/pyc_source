# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_mailchimp_forms/models.py
# Compiled at: 2010-11-29 14:27:26
from django.contrib.auth.models import User
from django.db import models

class MailingList(models.Model):
    user = models.OneToOneField(User, blank=False, null=False)
    confirmed = models.BooleanField(default=False)