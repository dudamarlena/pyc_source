# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maupetit/projects/TailorDev/django-tailordev-biblio/sandbox/urls.py
# Compiled at: 2018-11-13 15:51:41
# Size of source mod 2**32: 273 bytes
"""td_biblio urls"""
from django.conf.urls import include, url
from django.contrib import admin
urlpatterns = [
 url('^admin/', admin.site.urls),
 url('^auth/', include('django.contrib.auth.urls')),
 url('^', include('td_biblio.urls', namespace='td_biblio'))]