# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/urls.py
# Compiled at: 2015-01-18 13:17:01
# Size of source mod 2**32: 713 bytes
from django.conf.urls import patterns, url, include
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView
from kii.app import core
kii_urls = core.apps.get_apps_urls()
kii_api_urls = core.apps.get_apps_urls('api_urls')
all_kii_urls = patterns('', url('^api/', include(kii_api_urls, namespace='api')), url('^u/(?P<username>\\w+)/', include(kii_urls, namespace='user_area')), url('^', include(kii_urls)), url('^$', RedirectView.as_view(url=reverse_lazy('kii:stream:index'), permanent=False)))
urlpatterns = patterns('', url('^activity/', include('actstream.urls')), url('^', include(all_kii_urls, namespace='kii')))