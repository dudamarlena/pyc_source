# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bharadwaj/Desktop/django-celery/tests/someapp/tasks.py
# Compiled at: 2016-04-14 06:58:51
from celery.task import task
from django.apps import apps

@task(name='c.unittest.SomeAppTask')
def SomeAppTask(**kwargs):
    return 42


@task(name='c.unittest.SomeModelTask')
def SomeModelTask(pk):
    model = apps.get_model('someapp', 'Thing')
    thing = model.objects.get(pk=pk)
    return thing.name