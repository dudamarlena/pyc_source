# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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