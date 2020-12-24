# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/option.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
from django.db import models
from django.utils import timezone
from sentry.db.models import Model, sane_repr
from sentry.db.models.fields import EncryptedPickledObjectField

class Option(Model):
    """
    Global options which apply in most situations as defaults,
    and generally can be overwritten by per-project options.

    Options which are specific to a plugin should namespace
    their key. e.g. key='myplugin:optname'
    """
    __core__ = True
    key = models.CharField(max_length=64, unique=True)
    value = EncryptedPickledObjectField()
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_option'

    __repr__ = sane_repr('key', 'value')