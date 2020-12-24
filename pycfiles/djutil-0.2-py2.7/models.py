# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\djutil\models.py
# Compiled at: 2013-08-27 09:32:27
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(_(b'Created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_(b'Modified at'), auto_now=True)

    class Meta:
        abstract = True


class AuthorTimeStampedModel(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(b'Created by'), null=True, blank=True, on_delete=models.SET_NULL, editable=False, related_name=b'+')
    created_at = models.DateTimeField(_(b'Created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_(b'Modified at'), auto_now=True)

    class Meta:
        abstract = True


def get_or_none(qs, *args, **kwargs):
    try:
        return qs.get(*args, **kwargs)
    except models.ObjectDoesNotExist:
        return

    return