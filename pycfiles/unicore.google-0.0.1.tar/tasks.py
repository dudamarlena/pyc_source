# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/universalcore/unicore.google/unicore/google/tasks.py
# Compiled at: 2015-01-20 08:03:45
from celery.task import task
from UniversalAnalytics import Tracker

@task(ignore_result=True)
def pageview(profile_id, client_id, data):
    tracker = Tracker.create(profile_id, client_id=client_id, user_agent=data.pop('user_agent'))
    tracker.send('pageview', data)