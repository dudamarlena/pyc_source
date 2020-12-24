# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/scaler/urls.py
# Compiled at: 2012-05-30 07:38:44
from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('', url('^$', 'django.views.generic.simple.direct_to_template', {'template': 'scaler/test.html'}, name='scaler-test'), url('^scaler-test-one/$', 'django.views.generic.simple.direct_to_template', {'template': 'scaler/test.html'}, name='scaler-test-one'), url('^scaler-test-two/$', 'django.views.generic.simple.direct_to_template', {'template': 'scaler/test.html'}, name='scaler-test-two'), url('^server-busy/$', 'django.views.generic.simple.direct_to_template', {'template': 'scaler/server_busy.html'}, name='server-busy'))