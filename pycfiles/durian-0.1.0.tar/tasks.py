# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/devel/durian/durian/tasks.py
# Compiled at: 2009-09-12 10:38:49
from celery.task.base import Task
from celery.registry import tasks
from celery.exceptions import MaxRetriesExceededError
from anyjson import serialize

class WebhookSignal(Task):
    """The default web hook action. Simply sends the payload to the
    listener URL as POST data.

    Task arguments

        * url
            The listener destination URL to send payload to.

        * payload
            The payload to send to the listener.

    """
    name = 'durian.tasks.WebhookSignal'
    ignore_result = True

    def run(self, url, payload, **kwargs):
        import urllib2, socket
        orig_timeout = socket.getdefaulttimeout()
        retry = kwargs.get('retry', False)
        fail_silently = kwargs.get('fail_silently', False)
        self.max_retries = kwargs.get('max_retries', self.max_retries)
        timeout = kwargs.get('timeout', orig_timeout)
        socket.setdefaulttimeout(timeout)
        try:
            try:
                urllib2.urlopen(url, serialize(payload))
            except urllib2.URLError, exc:
                if self.retry:
                    try:
                        self.retry(args=[url, payload], kwargs=kwargs, exc=exc)
                    except MaxRetriesExceededError:
                        if self.fail_silently:
                            return
                        raise

                else:
                    if fail_silently:
                        return
                    raise

        finally:
            socket.setdefaulttimeout(orig_timeout)