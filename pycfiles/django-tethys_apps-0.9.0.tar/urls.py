# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swainn/projects/tethysdev/django-tethys_apps/tethys_apps/urls.py
# Compiled at: 2014-09-04 17:04:06
from django.conf.urls import patterns, url, include
from tethys_apps.utilities import generate_app_url_patterns
urlpatterns = patterns('', url('^$', 'tethys_apps.views.library', name='app_library'))
app_url_patterns = generate_app_url_patterns()
for namespace, urls in app_url_patterns.iteritems():
    root_pattern = ('^{0}/').format(namespace.replace('_', '-'))
    urlpatterns.append(url(root_pattern, include(urls, namespace=namespace)))