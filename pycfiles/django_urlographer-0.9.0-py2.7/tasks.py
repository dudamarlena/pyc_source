# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/urlographer/tasks.py
# Compiled at: 2013-06-26 14:11:51
from celery.decorators import task
from django.test.client import RequestFactory
from urlographer.views import sitemap

@task(ignore_result=True)
def update_sitemap_cache():
    factory = RequestFactory()
    request = factory.get('/sitemap.xml')
    sitemap(request, invalidate_cache=True)