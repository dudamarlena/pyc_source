# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/idm/Work/flask-diamond/flask_diamond/facets/task_queue.py
# Compiled at: 2016-11-26 10:59:31
from flask_celery import Celery
celery = Celery()

def init_task_queue(self):
    """
    Initialize celery.
    """
    celery.init_app(self.app)