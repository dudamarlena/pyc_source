# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/userpermission.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
from django.db import models
from sentry.db.models import Model, FlexibleForeignKey, sane_repr

class UserPermission(Model):
    __core__ = True
    user = FlexibleForeignKey('sentry.User')
    permission = models.CharField(max_length=32)

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_userpermission'
        unique_together = (('user', 'permission'), )

    __repr__ = sane_repr('user_id', 'permission')

    @classmethod
    def for_user(cls, user_id):
        return frozenset(cls.objects.filter(user=user_id).values_list('permission', flat=True))