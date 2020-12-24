# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/4f/p6rdjlq11nz2jwrtdlm918l40000gn/T/pip-install-tisqp5jr/django-currencyware/currencyware/tests/urls.py
# Compiled at: 2018-08-22 09:57:42
# Size of source mod 2**32: 264 bytes
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.sites.models import Site
admin.autodiscover()
Site.objects.get_or_create(name='unittest', domain='unitest.org')
urlpatterns = [
 url('^admin/', admin.site.urls)]