# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/regioninfo.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 6214 bytes
import os, boto
from boto.compat import json
from boto.exception import BotoClientError

def load_endpoint_json(path):
    """
    Loads a given JSON file & returns it.

    :param path: The path to the JSON file
    :type path: string

    :returns: The loaded data
    """
    with open(path, 'r') as (endpoints_file):
        return json.load(endpoints_file)


def merge_endpoints(defaults, additions):
    """
    Given an existing set of endpoint data, this will deep-update it with
    any similarly structured data in the additions.

    :param defaults: The existing endpoints data
    :type defaults: dict

    :param defaults: The additional endpoints data
    :type defaults: dict

    :returns: The modified endpoints data
    :rtype: dict
    """
    for service, region_info in additions.items():
        defaults.setdefault(service, {})
        defaults[service].update(region_info)

    return defaults


def load_regions():
    """
    Actually load the region/endpoint information from the JSON files.

    By default, this loads from the default included ``boto/endpoints.json``
    file.

    Users can override/extend this by supplying either a ``BOTO_ENDPOINTS``
    environment variable or a ``endpoints_path`` config variable, either of
    which should be an absolute path to the user's JSON file.

    :returns: The endpoints data
    :rtype: dict
    """
    endpoints = load_endpoint_json(boto.ENDPOINTS_PATH)
    additional_path = None
    if os.environ.get('BOTO_ENDPOINTS'):
        additional_path = os.environ['BOTO_ENDPOINTS']
    elif boto.config.get('Boto', 'endpoints_path'):
        additional_path = boto.config.get('Boto', 'endpoints_path')
    if additional_path:
        additional = load_endpoint_json(additional_path)
        endpoints = merge_endpoints(endpoints, additional)
    return endpoints


def get_regions(service_name, region_cls=None, connection_cls=None):
    """
    Given a service name (like ``ec2``), returns a list of ``RegionInfo``
    objects for that service.

    This leverages the ``endpoints.json`` file (+ optional user overrides) to
    configure/construct all the objects.

    :param service_name: The name of the service to construct the ``RegionInfo``
        objects for. Ex: ``ec2``, ``s3``, ``sns``, etc.
    :type service_name: string

    :param region_cls: (Optional) The class to use when constructing. By
        default, this is ``RegionInfo``.
    :type region_cls: class

    :param connection_cls: (Optional) The connection class for the
        ``RegionInfo`` object. Providing this allows the ``connect`` method on
        the ``RegionInfo`` to work. Default is ``None`` (no connection).
    :type connection_cls: class

    :returns: A list of configured ``RegionInfo`` objects
    :rtype: list
    """
    endpoints = load_regions()
    if service_name not in endpoints:
        raise BotoClientError("Service '%s' not found in endpoints." % service_name)
    if region_cls is None:
        region_cls = RegionInfo
    region_objs = []
    for region_name, endpoint in endpoints.get(service_name, {}).items():
        region_objs.append(region_cls(name=region_name, endpoint=endpoint, connection_cls=connection_cls))

    return region_objs


class RegionInfo(object):
    __doc__ = '\n    Represents an AWS Region\n    '

    def __init__(self, connection=None, name=None, endpoint=None, connection_cls=None):
        self.connection = connection
        self.name = name
        self.endpoint = endpoint
        self.connection_cls = connection_cls

    def __repr__(self):
        return 'RegionInfo:%s' % self.name

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'regionName':
            self.name = value
        else:
            if name == 'regionEndpoint':
                self.endpoint = value
            else:
                setattr(self, name, value)

    def connect(self, **kw_params):
        """
        Connect to this Region's endpoint. Returns an connection
        object pointing to the endpoint associated with this region.
        You may pass any of the arguments accepted by the connection
        class's constructor as keyword arguments and they will be
        passed along to the connection object.

        :rtype: Connection object
        :return: The connection to this regions endpoint
        """
        if self.connection_cls:
            return self.connection_cls(region=self, **kw_params)