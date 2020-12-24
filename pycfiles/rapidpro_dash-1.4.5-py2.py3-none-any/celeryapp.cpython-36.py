# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rowan/Nyaruka/dash/dash_test_runner/celeryapp.py
# Compiled at: 2017-04-17 16:26:07
# Size of source mod 2**32: 446 bytes
from __future__ import unicode_literals, print_function
import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dash_test_runner.settings')
from django.conf import settings
app = Celery('dash_test_runner')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))