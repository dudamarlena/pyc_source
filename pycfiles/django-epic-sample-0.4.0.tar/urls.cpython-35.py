# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data1/home/davidm/egauge/django-epic-sample/epic-sample/epic-sample/urls.py
# Compiled at: 2016-11-07 23:53:01
# Size of source mod 2**32: 457 bytes
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
urlpatterns = [
 url('^admin/', include(admin.site.urls)),
 url('^epic/', include('epic.urls', namespace='epic'))] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)