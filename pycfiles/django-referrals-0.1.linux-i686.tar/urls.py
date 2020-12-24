# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/craterdome/work/magikally/lib/python2.7/site-packages/referrals/urls.py
# Compiled at: 2011-12-20 21:11:43
from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
urlpatterns = patterns('referrals.views', url('^refer/(?P<unique_key>[A-Za-z0-9_-]+)/$', 'refer', name='referral_refer'), url('^my-referrals/$', TemplateView.as_view(template_name='referrals/mine.html'), name='referral_mine'))