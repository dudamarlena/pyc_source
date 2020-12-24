# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/PythonNest/pythonnest/root_urls.py
# Compiled at: 2017-07-10 01:59:22
# Size of source mod 2**32: 1383 bytes
from django.conf.urls import url
from pythonnest import views
from pythonnest.views import xmlrpc
__author__ = 'Matthieu Gallet'
app_name = 'pythonnest'
urls = [
 url('^index\\.html$', views.index),
 url('^packages/(?P<order_by>(\\-modification|normalized_name))\\.html$', (views.all_packages), name='all_packages'),
 url('^package/(?P<package_id>\\d+)/(?P<release_id>\\d+)\\.html$', (views.show_package), name='show_package'),
 url('^package/(?P<package_id>\\d+)\\.html$', (views.show_package), name='show_package'),
 url('^pages/delete_role/(?P<role_id>\\d+)\\.html$', (views.delete_role), name='delete_role'),
 url('^pages/delete_download/(?P<download_id>\\d+)\\.html$', (views.delete_download), name='delete_download'),
 url('^pages/show_classifier/(?P<classifier_id>\\d+)\\.html$', (views.show_classifier), name='show_classifier'),
 url('^pypi/(?P<package_name>[^/]+)/json$', (views.package_json), name='package_json'),
 url('^pypi/(?P<package_name>[^/]+)/(?P<version>[^/]+)/json$', (views.version_json), name='version_json'),
 url('^pypi/?$', xmlrpc, name='rpc4django'),
 url('^simple/(?P<package_name>[^/]+)/(?P<version>[^/]+)$', (views.simple), name='simple'),
 url('^simple/(?P<package_name>[^/]+)/$', (views.simple), name='simple'),
 url('^simple/$', (views.simple), name='simple'),
 url('^setup/?$', (views.setup), name='setup')]