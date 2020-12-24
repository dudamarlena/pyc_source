# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/www/gunicorn_config.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1034 bytes
import setproctitle
from airflow import settings

def post_worker_init(dummy_worker):
    setproctitle.setproctitle(settings.GUNICORN_WORKER_READY_PREFIX + setproctitle.getproctitle())