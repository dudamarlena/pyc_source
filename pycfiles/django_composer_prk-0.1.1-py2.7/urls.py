# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/composer/tests/urls.py
# Compiled at: 2017-10-20 11:35:08
from django.conf.urls import url, include
from django.views.generic.base import TemplateView
from composer.tests.views import DummyModel1View
urlpatterns = [
 url('^$', TemplateView.as_view(template_name='tests/home.html'), name='home'),
 url('^dummymodel1/(?P<pk>\\d+)/$', DummyModel1View.as_view(), name='dummymodel1-detail'),
 url('^header/$', TemplateView.as_view(template_name='tests/header.html'), name='header'),
 url('^aaa/$', TemplateView.as_view(template_name='tests/aaa.html'), name='aaa'),
 url('^aaa/bbb/$', TemplateView.as_view(template_name='tests/bbb.html'), name='bbb'),
 url('^slot-context/$', TemplateView.as_view(template_name='tests/slot_context.html'), name='slot_context')]