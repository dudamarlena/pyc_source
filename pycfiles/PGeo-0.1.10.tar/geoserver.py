# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kalimaha/Development/git-repositories/Geobricks/pgeo/pgeo/geoserver/geoserver.py
# Compiled at: 2014-08-04 05:19:09
import httplib2
from urlparse import urlparse
from pgeo.geoserver.gsutils import url, prepare_upload_bundle
from pgeo.db.postgresql.postgis_utils import shapefile
from pgeo.utils import log
from pgeo.error.custom_exceptions import PGeoException, errors
log = log.logger(__name__)

class Geoserver():
    config = None

    def __init__(self, config, disable_ssl_certificate_validation=False):
        """
        Initialize and configure the GeoServer.
        The GeoServer properties are passed in the config file
        """
        self.config = config
        self.service_url = self.config['geoserver_master']
        self.username = self.config['username']
        self.password = self.config['password']
        if self.service_url.endswith('/'):
            self.service_url = self.service_url.strip('/')
        self.http = httplib2.Http(disable_ssl_certificate_validation=disable_ssl_certificate_validation)
        self.http.add_credentials(self.username, self.password)
        netloc = urlparse(self.service_url).netloc
        self.http.authorizations.append(httplib2.BasicAuthentication((
         self.username, self.password), netloc, self.service_url, {}, None, None, self.http))
        self._cache = dict()
        self._version = None
        return

    def publish_coveragestore(self, data, overwrite=False):
        name = data['name']
        workspace = self.get_default_workspace() if 'workspace' not in data else data['workspace']
        path = data['path']
        if not overwrite:
            if self.check_if_coveragestore_exist(name, workspace):
                raise PGeoException(errors[520] + ': %s' % name)
        headers = get_headers('geotiff')
        archive = None
        ext = 'geotiff'
        if isinstance(path, dict):
            archive = prepare_upload_bundle(name, path)
            print archive
            message = open(archive, 'rb')
            if 'tfw' in path:
                headers = get_headers('archive')
                ext = 'worldimage'
        elif isinstance(path, basestring):
            message = open(path, 'rb')
        else:
            message = path
        log.info(message)
        try:
            headers = get_headers('tiff')
            cs_url = url(self.service_url, ['workspaces', workspace, 'coveragestores', name, 'file.' + ext])
            self._publish_coveragestore(cs_url, 'PUT', message, headers)
            json_data = data
            del json_data['name']
            self.update_layer_metadata(name, json_data, 'json')
        finally:
            self.reload_configuration_geoserver_slaves()
            return True

        return True

    def _publish_coveragestore(self, cs_url, type, message, headers):
        log.info(cs_url)
        try:
            headers, response = self.http.request(cs_url, type, message, headers)
            self._cache.clear()
            log.info(headers)
            log.info(response)
            if headers.status != 201:
                log.info(headers)
                log.info(response)
                raise PGeoException(response, headers.status)
        finally:
            if hasattr(message, 'close'):
                self.reload_configuration_geoserver_slaves()
                message.close()
                return True

    def update_layer_metadata(self, name, data, c_type='json'):
        """
        Update the layer by json or xml
        :param name: name of the layer
        :type name: string
        :param data: json
        :type name: string cointaining the data to update i.e. json '{"layer":{"title":"title of the layer"}}' or xml <layer><title>title of the layer</title></layer>
        :param type: string that can be "json" or "xml"
        :type name: string
        :return: True if updated
        """
        try:
            headers = get_headers(c_type)
            cs_url = url(self.service_url, ['layers', name + '.' + c_type])
            self._publish_coveragestore(cs_url, 'PUT', data, headers)
        finally:
            self.reload_configuration_geoserver_slaves()
            return True

    def delete_coveragestore(self, name, workspace=None, purge=True, recurse=True):
        if workspace is None:
            workspace = self.get_default_workspace()
        if self.check_if_coveragestore_exist(name, workspace):
            cs_url = url(self.service_url, ['workspaces', workspace, 'coveragestores', name])
            return self.delete(cs_url, purge, recurse)
        else:
            return

    def delete(self, rest_url, purge=False, recurse=False):
        """
        send a delete request
        """
        params = []
        if purge:
            params.append('purge=true')
        if recurse:
            params.append('recurse=true')
        if params:
            rest_url = rest_url + '?' + ('&').join(params)
        headers = get_headers('xml')
        response, content = self.http.request(rest_url, 'DELETE', headers=headers)
        self._cache.clear()
        if response.status == 200:
            self.reload_configuration_geoserver_slaves()
            return True
        raise PGeoException(content, headers.status)

    def check_if_coveragestore_exist(self, name, workspace=None):
        if workspace is None:
            workspace = self.get_default_workspace()
        cs_url = url(self.service_url, ['workspaces', workspace, 'coveragestores', name])
        response, content = self.http.request(cs_url, 'GET')
        if response.status == 200:
            return True
        else:
            if response.status == 404:
                return False
            return False

    def set_default_style(self, layername, stylename, enabled=True):
        """
        Method used to change the default style of a layer
        :param stylename: the name of the style to set ad default one
        :param layername: the name of the layer
        :param enabled: enable/disable the style
        :return:
        """
        headers = {'Content-type': 'application/xml', 
           'Accept': 'application/xml'}
        print layername
        xml = ('<layer><defaultStyle><name>{0}</name></defaultStyle><enabled>{1}</enabled></layer>').format(unicode(stylename).lower(), unicode(str(enabled).upper()))
        cs_url = url(self.service_url, ['layers', layername])
        headers, response = self.http.request(cs_url, 'PUT', xml, headers)
        print cs_url
        if headers.status == 200:
            self.reload_configuration_geoserver_slaves()
            return True
        else:
            print headers.status, ' ', response
            return False

    def publish_shapefile(self, input_shapefile, name, overwrite=False, workspace=None, projection=None, default_style=None, layertype=None, metadata=None):
        """
        :param input_shapefile:
        :param name:
        :param overwrite:
        :param workspace:
        :param projection:
        :param default_style:
        :param layertype:
        :param metadata:
        :return:
        """
        datasource = self.get_default_datasource()
        shapefile.import_shapefile(datasource, input_shapefile, name)
        self.publish_postgis_table(datasource, name)
        return 'published'

    def publish_postgis_table(self, datasource, name):
        """
        :param datasource: datasource stored in geoserver
        :param name: name of the table in postgis
        :return:
        """
        headers = {'Content-type': 'application/xml', 
           'Accept': 'application/xml'}
        xml = ('<featureType><name>{0}</name></featureType>').format(unicode(name).lower())
        cs_url = url(self.service_url, ['workspaces', datasource['workspace'], 'datasources', datasource['datasource'], 'featuretypes'])
        headers, response = self.http.request(cs_url, 'POST', xml, headers)
        log.info(headers)
        if headers.status == 201:
            self.reload_configuration_geoserver_slaves()
            return True
        else:
            return False

    def checkIFdatasourceExist(self, name):
        print 'TODO'

    def get_default_workspace(self):
        return self.get('default_workspace')

    def get_default_datasource(self):
        default_datasource = self.config['default_datasource']
        print default_datasource
        datasource = self.config['datasources']
        for d in datasource:
            if default_datasource in d['datasource']:
                return d

        return False

    def reload_configuration_geoserver_slaves(self, force_master_reload=False):
        geoserver_cluster = self.config['geoserver_slaves']
        if force_master_reload is True:
            geoserver_cluster.append(self.config['geoserver_master'])
        for geoserver in geoserver_cluster:
            cs_url = url(geoserver, ['reload?recurse=true'])
            headers, response = self.http.request(cs_url, 'POST')
            log.info(headers)
            if headers.status == 200:
                return True
            return False


def get_headers(c_type):
    c_type = c_type.lower()
    headers = {'Accept': 'application/xml'}
    if c_type == 'geotiff':
        headers['Content-type'] = 'image/tiff'
    elif c_type == 'tiff':
        headers['Content-type'] = 'image/tiff'
    elif c_type == 'xml':
        headers['Content-type'] = 'application/xml'
    elif c_type == 'json':
        headers['Content-type'] = 'application/json'
    elif c_type == 'archive':
        headers['Content-type'] = 'application/archive'
    else:
        raise PGeoException('Headers type "%s" not supported' % type)
    return headers