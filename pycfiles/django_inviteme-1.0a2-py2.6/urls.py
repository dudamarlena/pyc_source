# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/inviteme/urls.py
# Compiled at: 2012-04-10 19:26:08
from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('inviteme.views', url('^$', 'get_form', name='inviteme-get-form'), url('^post/$', 'post_form', name='inviteme-post-form'), url('^confirm/(?P<key>[^/]+)$', 'confirm_mail', name='inviteme-confirm-mail'))