# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/silly/dev/django-object-tools/object_tools/tests/urls.py
# Compiled at: 2018-12-21 04:58:46
# Size of source mod 2**32: 604 bytes
import django, object_tools
from django.contrib import admin
if django.VERSION >= (2, 0):
    from django.urls import path
    urlpatterns = [
     path('admin/', admin.site.urls),
     path('object-tools/', object_tools.tools.urls)]
else:
    try:
        from django.conf.urls.defaults import include, url
    except ImportError:
        from django.conf.urls import include, url

    admin.autodiscover()
    object_tools.autodiscover()
    urlpatterns = [
     url('^admin/', include(admin.site.urls)),
     url('^object-tools/', include(object_tools.tools.urls))]