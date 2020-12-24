# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/brent/anaconda/envs/fba/lib/python2.7/site-packages/examples/django_celery/proj/celery.py
# Compiled at: 2014-08-09 13:41:56
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'examples.django_celery.proj.settings')
app = Celery('proj')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print ('Request: {0!r}').format(self.request)