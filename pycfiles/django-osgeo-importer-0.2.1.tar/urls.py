# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/importer/osgeo_importer/urls.py
# Compiled at: 2016-07-18 17:07:14
from django.conf.urls import patterns, url, include
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .views import FileAddView, UploadListView
from tastypie.api import Api
from .api import UploadedDataResource, UploadedLayerResource, UploadedFileResource
if getattr(settings, 'OSGEO_IMPORTER_GEONODE_ENABLED', False):
    from .geonode_apis import UploadedDataResource, UploadedLayerResource, UploadedFileResource
importer_api = Api(api_name='importer-api')
importer_api.register(UploadedDataResource())
importer_api.register(UploadedLayerResource())
importer_api.register(UploadedFileResource())
urlpatterns = patterns('', url('^uploads/new$', login_required(FileAddView.as_view()), name='uploads-new'), url('^uploads/new/json$', login_required(FileAddView.as_view(json=True)), name='uploads-new-json'), url('^uploads/?$', login_required(UploadListView.as_view()), name='uploads-list'), url('', include(importer_api.urls)))