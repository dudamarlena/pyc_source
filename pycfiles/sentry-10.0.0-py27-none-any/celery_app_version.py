# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/status_checks/celery_app_version.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import sentry
from django.conf import settings
from sentry import options
from .base import StatusCheck, Problem

class CeleryAppVersionCheck(StatusCheck):

    def check(self):
        if settings.CELERY_ALWAYS_EAGER:
            return []
        version = options.get('sentry:last_worker_version')
        if not version:
            return []
        if version == sentry.VERSION:
            return []
        return [
         Problem(('Celery workers are referencing a different version of Sentry ({version1} vs {version2})').format(version1=sentry.VERSION, version2=version))]