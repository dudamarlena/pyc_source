# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/liveblog/tasks.py
# Compiled at: 2016-09-28 11:20:42
# Size of source mod 2**32: 1932 bytes
from celery import shared_task
import requests
from django.conf import settings

def _get_entry_url(liveblog_id, entry_id):
    endpoint = getattr(settings, 'LIVEBLOG_FIREBASE_NOTIFY_ENTRY_ENDPOINT', None)
    if endpoint:
        return endpoint.format(liveblog_id=liveblog_id, entry_id=entry_id)


@shared_task(default_retry_delay=5)
def firebase_update_entry(liveblog_id, entry_id, published):
    url = _get_entry_url(liveblog_id, entry_id)
    if url:
        entry = {'id': entry_id}
        if published:
            entry['published'] = published.isoformat()
        resp = requests.patch(url, json=entry)
        resp.raise_for_status()


@shared_task(default_retry_delay=5)
def firebase_delete_entry(liveblog_id, entry_id):
    url = _get_entry_url(liveblog_id, entry_id)
    if url:
        resp = requests.delete(url)
        resp.raise_for_status()


@shared_task(default_retry_delay=5)
def firebase_delete_liveblog(liveblog_id):
    endpoint = getattr(settings, 'LIVEBLOG_FIREBASE_NOTIFY_ENTRIES_ENDPOINT', None)
    if endpoint:
        url = endpoint.format(liveblog_id=liveblog_id)
        resp = requests.delete(url)
        resp.raise_for_status()