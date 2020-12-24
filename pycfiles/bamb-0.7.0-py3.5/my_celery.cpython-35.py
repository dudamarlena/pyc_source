# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/web/my_celery.py
# Compiled at: 2017-09-08 11:08:24
# Size of source mod 2**32: 748 bytes
from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
from web import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
app = Celery('web')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))