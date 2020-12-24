# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yohann/Dev/django-pg-badges/demo/venv/lib/python2.7/site-packages/badges/models.py
# Compiled at: 2016-01-24 17:14:04
from __future__ import unicode_literals
from django.conf import settings
from django.db import models

class Badge(models.Model):
    """
    Badges are earned by users for doing nice things.
    They earn the badge when as a `condition` is meet.

    Badges and conditions are set in the badge.json file.  Here we
    only link a user to a badge.
    Badges are uniquely identified by a code.
    A User cannot have the same badge twice.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.TextField()
    code = models.CharField(max_length=100)

    class Meta:
        unique_together = ('user', 'name')