# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superhero/urls.py
# Compiled at: 2015-05-05 00:01:33
from django.conf.urls import patterns, url
from jmbo.views import ObjectDetail
urlpatterns = patterns('', url('^(?P<slug>[\\w-]+)/$', ObjectDetail.as_view(), name='superhero_object_detail'))