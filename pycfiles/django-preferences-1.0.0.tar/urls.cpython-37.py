# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/silly/dev/django-preferences/preferences/tests/urls.py
# Compiled at: 2018-12-20 02:32:17
# Size of source mod 2**32: 154 bytes
from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()
urlpatterns = [
 url('^admin/', admin.site.urls)]