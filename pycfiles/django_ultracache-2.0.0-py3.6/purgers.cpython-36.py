# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ultracache/purgers.py
# Compiled at: 2018-09-10 07:18:29
# Size of source mod 2**32: 1006 bytes
import requests
from django.conf import settings

def broadcast(path, headers=None):
    from ultracache.tasks import broadcast_purge
    broadcast_purge.delay(path, headers)


def varnish(path, headers=None):
    loc = settings.ULTRACACHE['purge']['method']['url'].rstrip('/') + '/' + path.lstrip('/')
    try:
        r = requests.request('PURGE', loc, timeout=1, headers=(headers or {}))
    except requests.exceptions.RequestException:
        pass


def nginx(path, headers=None):
    loc = settings.ULTRACACHE['purge']['method']['url'].rstrip('/') + '/' + path.lstrip('/')
    try:
        r = requests.request('PURGE', loc, timeout=1, headers=(headers or {}))
    except requests.exceptions.RequestException:
        pass