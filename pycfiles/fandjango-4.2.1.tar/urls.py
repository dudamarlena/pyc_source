# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jgorset/Code/python/fandjango/fandjango/urls.py
# Compiled at: 2015-12-28 07:16:58
try:
    from django.conf.urls.defaults import patterns, url
except:
    from django.conf.urls import patterns, url

from views import *
urlpatterns = patterns('', url('^authorize_application.html$', authorize_application, name='authorize_application'), url('^deauthorize_application.html$', deauthorize_application, name='deauthorize_application'))