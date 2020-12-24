# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_mailchimp_forms/urls.py
# Compiled at: 2010-11-29 14:27:26
from django.conf.urls.defaults import *
from django_mailchimp_forms.views import chimpy_register, chimpy_unregister
urlpatterns = patterns('', url('^register/$', chimpy_register, name='chimpy_register'), url('^unregister/$', chimpy_unregister, name='chimpy_unregister'))