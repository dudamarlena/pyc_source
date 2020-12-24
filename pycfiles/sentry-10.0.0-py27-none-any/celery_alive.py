# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/status_checks/celery_alive.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from time import time
from django.conf import settings
from sentry import options
from sentry.utils.http import absolute_uri
from .base import Problem, StatusCheck

class CeleryAliveCheck(StatusCheck):

    def check(self):
        if settings.CELERY_ALWAYS_EAGER:
            return []
        else:
            last_ping = options.get('sentry:last_worker_ping') or 0
            if last_ping >= time() - 300:
                return []
            backlogged, size = (None, 0)
            from sentry.monitoring.queues import backend
            if backend is not None:
                size = backend.get_size('default')
                backlogged = size > 0
            message = "Background workers haven't checked in recently. "
            if backlogged:
                message += "It seems that you have a backlog of %d tasks. Either your workers aren't running or you need more capacity." % size
            else:
                message += "This is likely an issue with your configuration or the workers aren't running."
            return [
             Problem(message, url=absolute_uri('/manage/queue/'))]