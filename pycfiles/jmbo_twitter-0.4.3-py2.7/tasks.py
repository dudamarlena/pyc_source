# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo_twitter/tasks.py
# Compiled at: 2014-12-22 06:58:24
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from jmbo_twitter.models import Feed, Search

@periodic_task(run_every=crontab(hour='*', minute='*/15', day_of_week='*'), ignore_result=True)
def fetch_feeds():
    for feed in Feed.objects.all():
        feed.fetch(force=True)


@periodic_task(run_every=crontab(hour='*', minute='*/15', day_of_week='*'), ignore_result=True)
def fetch_searchs():
    for search in Search.objects.all():
        search.fetch(force=True)