# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe/monitoring.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 769 bytes
from django.conf import settings
from django.core.cache import cache
from django.db import connections
from django.db.utils import OperationalError

def get_status():
    return {'database': check_database(), 
     'cache': check_cache()}


def check_database():
    db_conn = connections['default']
    try:
        db_conn.cursor()
    except OperationalError:
        connected = False
    else:
        connected = True
    return connected


def check_cache():
    if 'DummyCache' in settings.CACHES['default']['BACKEND']:
        return True
        try:
            cache.set('_cms_qe_monitoring', 'test', 5)
            return cache.get('_cms_qe_monitoring') == 'test'
        except Exception as exc:
            return str(exc)