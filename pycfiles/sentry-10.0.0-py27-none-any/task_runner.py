# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/byk/Documents/Projects/sentry/sentry/src/sentry/testutils/helpers/task_runner.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
__all__ = ['TaskRunner']
from celery import current_app
from contextlib import contextmanager
from django.conf import settings

@contextmanager
def TaskRunner():
    settings.CELERY_ALWAYS_EAGER = True
    current_app.conf.CELERY_ALWAYS_EAGER = True
    yield
    current_app.conf.CELERY_ALWAYS_EAGER = False
    settings.CELERY_ALWAYS_EAGER = False