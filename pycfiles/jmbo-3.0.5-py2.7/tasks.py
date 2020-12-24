# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/tasks.py
# Compiled at: 2016-03-08 06:26:22
from django.db.models import Q
from django.utils import timezone
from celery import task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from jmbo.models import ModelBase

@periodic_task(run_every=crontab(hour='*', minute='*/10', day_of_week='*'), ignore_result=True)
def publish_scheduled_content():
    now = timezone.now()
    q1 = Q(publish_on__lte=now, retract_on__isnull=True)
    q2 = Q(publish_on__lte=now, retract_on__gt=now)
    ModelBase.objects.filter(state='unpublished').filter(q1 | q2).update(state='published')
    ModelBase.objects.filter(state='published').filter(retract_on__lte=now).update(state='unpublished')