# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/HMFcalc/tasks.py
# Compiled at: 2013-06-13 03:28:42
"""
Created on Jun 12, 2013

@author: Steven
"""
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from time import time
from django.conf import settings

@periodic_task(run_every=crontab(hour='*', minute='*', day_of_week='*'))
def writefile():
    print 'Writing to file...'
    with open(settings.ROOT_DIR + '/heartbeat', 'a') as (f):
        f.write(str(time()))