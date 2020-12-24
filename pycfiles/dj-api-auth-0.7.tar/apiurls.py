# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fanfei/Documents/Code/dj-api-auth/example/djapp/djapp/apiurls.py
# Compiled at: 2015-06-06 18:52:29
from django.conf.urls import patterns, url
from djapiauth import url_with_auth
import apis
urlpatterns = patterns('', url_with_auth('^hello/$', 'djapp.views.index'), url('^goodbye/$', 'djapp.apis.apicall'), url('^classbased1/$', apis.ProtectedView.as_view()), url('^classbased2/$', apis.UnprotectedView.as_view()))