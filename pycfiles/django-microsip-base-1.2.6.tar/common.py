# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\django-microsip-base\django_microsip_base\django_microsip_base\urls\common.py
# Compiled at: 2019-09-09 14:23:54
import autocomplete_light
autocomplete_light.autodiscover()
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
urlpatterns = patterns('', url('', include('django_microsip_base.apps.main.urls', namespace='main')), url('', include('microsip_api.apps.config.urls', namespace='config')), url('administrador/', include('microsip_api.apps.administrador.urls', namespace='administrador')), url('autocomplete/', include('autocomplete_light.urls')), url('^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))
for plugin in settings.EXTRA_APPS:
    urlpatterns += (url('^' + plugin['url_main_path'], include(plugin['app'] + '.urls', namespace=plugin['url_main_path'])),)

urlpatterns += staticfiles_urlpatterns()