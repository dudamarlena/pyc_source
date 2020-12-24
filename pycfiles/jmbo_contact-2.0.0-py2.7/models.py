# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/contact/models.py
# Compiled at: 2015-04-21 15:31:42
from django.contrib.auth.models import User
from django.db import models
from preferences.models import Preferences

class ContactPreferences(Preferences):
    __module__ = 'preferences.models'
    telephone = models.CharField(max_length=24, blank=True, null=True)
    fax = models.CharField(max_length=24, blank=True, null=True)
    physical_address = models.TextField(blank=True, null=True)
    postal_address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    sms = models.CharField(max_length=24, blank=True, null=True)
    email_recipients = models.ManyToManyField(User, blank=True, null=True, help_text='Select users who will recieve emails sent via the general contact form.')

    class Meta:
        verbose_name = 'Contact preferences'
        verbose_name_plural = 'Contact preferences'