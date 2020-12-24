# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/catchbot/celery_app.py
# Compiled at: 2018-06-23 13:58:03
# Size of source mod 2**32: 452 bytes
import os
from celery import Celery

def _get_broker():
    return 'pyamqp://{user}:{password}@{host}/{vhost}'.format(host='rabbitmq:5672',
      user=(os.environ['RABBITMQ_DEFAULT_USER']),
      password=(os.environ['RABBITMQ_DEFAULT_PASS']),
      vhost=(os.environ['RABBITMQ_DEFAULT_VHOST']))


try:
    broker = _get_broker()
except:
    print('Failed to get celery broker')
    broker = None

app = Celery('tasks', broker=broker)