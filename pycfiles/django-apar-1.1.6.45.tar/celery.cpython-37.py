# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/celery.py
# Compiled at: 2020-01-05 09:49:44
# Size of source mod 2**32: 352 bytes
import os
from celery import Celery
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DJANGO_PROJECT.settings')
app = Celery('DJANGO_PROJECT')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.task_default_queue = os.path.basename(os.path.normpath(settings.BASE_DIR))
app.autodiscover_tasks()