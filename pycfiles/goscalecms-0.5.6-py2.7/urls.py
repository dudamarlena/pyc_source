# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/goscale/urls.py
# Compiled at: 2013-02-27 00:55:16
from django.conf.urls import patterns, url
from django.conf import settings
import views
urlpatterns = patterns('', url('^utils/form/$', views.form, name='goscale_form_handler'))
if 'allauth.account' in settings.INSTALLED_APPS:
    try:
        from allauth.account.views import signup
        urlpatterns += patterns('', url('^signup/$', signup, name='goscale_account_signup', kwargs={'template_name': 'user/signup.html'}))
    except ImportError:
        pass