# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/code/django-saltapi/django_saltapi/urls.py
# Compiled at: 2013-03-11 12:04:27
from django_saltapi.utils import REGEX_JID, REGEX_HOSTNAME
from django.conf.urls import patterns, url
urlpatterns = patterns('django_saltapi.views', url('^$', 'apiwrapper'), url('^minions/$', 'minions_list'), url('^minions/(?P<tgt>' + REGEX_HOSTNAME + ')/$', 'minions_details'), url('^jobs/$', 'jobs_list'), url('^jobs/(?P<jid>' + REGEX_JID + ')/$', 'jobs_details'), url('^ping/(?P<tgt>' + REGEX_HOSTNAME + ')/$', 'ping'), url('^echo/(?P<tgt>' + REGEX_HOSTNAME + ')/(?P<arg>\\w+)/$', 'echo'))