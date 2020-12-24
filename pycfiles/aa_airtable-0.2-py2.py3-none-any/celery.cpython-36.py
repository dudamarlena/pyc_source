# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./../aa_airtable/celery.py
# Compiled at: 2017-06-21 21:50:37
# Size of source mod 2**32: 264 bytes
from __future__ import absolute_import
from celery import Celery
from django.conf import settings
app = Celery('app.celery')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks((settings.INSTALLED_APPS), related_name='tasks')