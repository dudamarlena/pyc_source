# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/service_catalog.py
# Compiled at: 2016-06-13 14:11:03
import vsmclient.exceptions

class ServiceCatalog(object):
    """Helper methods for dealing with a Keystone Service Catalog."""

    def __init__(self, resource_dict):
        self.catalog = resource_dict

    def get_token(self):
        return self.catalog['access']['token']['id']

    def url_for(self, attr=None, filter_value=None, service_type=None, endpoint_type='publicURL', service_name=None, vsm_service_name=None):
        """Fetch the public URL from the Compute service for
        a particular endpoint attribute. If none given, return
        the first. See tests for sample service catalog."""
        matching_endpoints = []
        if 'endpoints' in self.catalog:
            for endpoint in self.catalog['endpoints']:
                if not filter_value or endpoint[attr] == filter_value:
                    matching_endpoints.append(endpoint)

            if not matching_endpoints:
                raise vsmclient.exceptions.EndpointNotFound()
        if 'serviceCatalog' not in self.catalog['access']:
            return
        else:
            catalog = self.catalog['access']['serviceCatalog']
            for service in catalog:
                if service.get('type') != service_type:
                    continue
                if service_name and service_type == 'compute' and service.get('name') != service_name:
                    continue
                if vsm_service_name and service_type == 'vsm' and service.get('name') != vsm_service_name:
                    continue
                endpoints = service['endpoints']
                for endpoint in endpoints:
                    if not filter_value or endpoint.get(attr) == filter_value:
                        endpoint['serviceName'] = service.get('name')
                        matching_endpoints.append(endpoint)

            if not matching_endpoints:
                raise vsmclient.exceptions.EndpointNotFound()
            elif len(matching_endpoints) > 1:
                raise vsmclient.exceptions.AmbiguousEndpoints(endpoints=matching_endpoints)
            else:
                return matching_endpoints[0][endpoint_type]
            return