# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/shared/Resource.py
# Compiled at: 2012-11-01 11:35:36
from vas.shared.Security import Security
from vas.util.LinkUtils import LinkUtils

class Resource(object):
    """The base of all types that interact with the REST API. A resource should map to a
    specific URI in the REST API.

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    @property
    def security(self):
        return self.__security

    @property
    def _client(self):
        return self.__client

    @property
    def _details(self):
        return self.__details

    @property
    def _location(self):
        return self.__location

    def __init__(self, client, location):
        self.__client = client
        self.__location = location
        self.reload()
        self.__security = self._create_resource_from_link('security', Security)

    def reload(self):
        """Reloads the resource's details from the server"""
        self.__details = self.__client.get(self.__location)

    def _create_resource_from_link(self, rel, resource_class):
        return resource_class(self.__client, LinkUtils.get_link_href(self.__details, rel))

    def _create_resources_from_links(self, rel, resource_class):
        return [ resource_class(self.__client, location) for location in LinkUtils.get_link_hrefs(self.__details, rel) ]

    def __eq__(self, other):
        return self.__location == other.__location

    def __hash__(self):
        return hash(self.__location)

    def __lt__(self, other):
        return self.__location < other.__location

    def __repr__(self):
        return ('{}(client={}, location={})').format(self.__class__.__name__, self._client, repr(self.__location))