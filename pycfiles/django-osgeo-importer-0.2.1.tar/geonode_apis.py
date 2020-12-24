# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/importer/osgeo_importer/geonode_apis.py
# Compiled at: 2016-09-22 18:31:21
import os
from .api import UserResource, UploadedLayerResource, UserOwnsObjectAuthorization, UploadedDataResource, MultipartResource, UploadedFileResource
from geonode.api.api import ProfileResource
from geonode.geoserver.helpers import ogc_server_settings
from tastypie.fields import ForeignKey

class UploadedDataResource(UploadedDataResource):
    """
    API for accessing UploadedData.
    """
    user = ForeignKey(ProfileResource, 'user')


class UploadedLayerResource(UploadedLayerResource):

    def clean_configuration_options(self, request, obj, configuration_options):
        if configuration_options.get('geoserver_store'):
            store = configuration_options.get('geoserver_store')
            if store.get('type', str).lower() == 'geogig':
                store.setdefault('branch', 'master')
                store.setdefault('create', 'true')
                store.setdefault('name', ('{0}-layers').format(request.user.username))
                store['geogig_repository'] = os.path.join(ogc_server_settings.GEOGIG_DATASTORE_DIR, store.get('name'))
        if not configuration_options.get('layer_owner'):
            configuration_options['layer_owner'] = obj.upload.user.username
        return configuration_options