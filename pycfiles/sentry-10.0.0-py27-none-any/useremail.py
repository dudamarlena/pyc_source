# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/receivers/useremail.py
# Compiled at: 2019-08-16 12:27:40
from __future__ import absolute_import
from django.db import IntegrityError
from django.db.models.signals import post_save
from sentry.models import User, UserEmail

def create_user_email(instance, created, **kwargs):
    if created:
        try:
            UserEmail.objects.create(email=instance.email, user=instance)
        except IntegrityError:
            pass


post_save.connect(create_user_email, sender=User, dispatch_uid='create_user_email', weak=False)