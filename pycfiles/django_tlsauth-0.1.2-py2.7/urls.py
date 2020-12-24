# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_tlsauth/urls.py
# Compiled at: 2013-03-24 20:35:29
from django.conf.urls import patterns, url
from views import renderUserForm, renderCSRForm, renderCert, showcsrs, certify, reject, testAuth
urlpatterns = patterns('', url('^register/$', renderUserForm), url('^certify/$', renderCSRForm), url('^cert/$', renderCert), url('^csrs/$', showcsrs), url('^sign/(?P<id>.+)$', certify), url('^reject/(?P<id>.+)$', reject), url('^test/$', testAuth))