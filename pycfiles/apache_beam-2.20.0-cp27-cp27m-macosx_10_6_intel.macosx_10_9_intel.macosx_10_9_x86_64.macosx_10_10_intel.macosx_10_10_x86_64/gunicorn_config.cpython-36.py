# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/www/gunicorn_config.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1034 bytes
import setproctitle
from airflow import settings

def post_worker_init(dummy_worker):
    setproctitle.setproctitle(settings.GUNICORN_WORKER_READY_PREFIX + setproctitle.getproctitle())