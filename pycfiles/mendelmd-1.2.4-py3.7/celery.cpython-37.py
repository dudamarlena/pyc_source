# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mendelmd/celery.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 854 bytes
from __future__ import absolute_import
import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mendelmd.settings')
from django.conf import settings
app = Celery('mendelmd')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)
app.conf.update(CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend')
app.conf.timezone = 'UTC'

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))