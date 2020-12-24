# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./../aa_airtable/celery.py
# Compiled at: 2017-06-21 21:50:37
# Size of source mod 2**32: 264 bytes
from __future__ import absolute_import
from celery import Celery
from django.conf import settings
app = Celery('app.celery')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks((settings.INSTALLED_APPS), related_name='tasks')