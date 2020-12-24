# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neo/urls.py
# Compiled at: 2013-03-14 09:30:20
from django.conf.urls.defaults import patterns, url, include
from foundry import forms
from neo.forms import NeoTokenGenerator, NeoPasswordChangeForm
neo_token_generator = NeoTokenGenerator()
urlpatterns = patterns('', url('^password_reset/$', 'django.contrib.auth.views.password_reset', {'password_reset_form': forms.PasswordResetForm, 
   'token_generator': neo_token_generator}, name='password_reset'), url('^password_change/$', 'django.contrib.auth.views.password_change', {'password_change_form': NeoPasswordChangeForm}, name='password_change'), url('^password_change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'), url('^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'), url('^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13})/$', 'django.contrib.auth.views.password_reset_confirm', {'token_generator': neo_token_generator}, name='password_reset_confirm'))