# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: urls.py
# Compiled at: 2011-06-19 19:04:51
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from project.utils.install import install_apps_urls
urlpatterns = patterns('')
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
install_apps_urls()