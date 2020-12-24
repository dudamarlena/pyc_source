# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/caps.py
# Compiled at: 2010-02-07 17:28:31
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
import urllib2
from types import *
from logging import getLogger
import re
from pyogp.lib.base.network.stdlib_client import StdLibClient, HTTPError
from pyogp.lib.base.exc import ResourceNotFound, ResourceError, DeserializerNotFound
from pyogp.lib.base.settings import Settings
from pyogp.lib.base.helpers import LLSDDeserializer, ListLLSDSerializer, DictLLSDSerializer
logger = getLogger('pyogp.lib.base.caps')

class Capability(object):
    """ models a capability 
    A capability is a web resource which enables functionality for a client
    The seed capability is a special type, through which other capabilities 
    are procured

    A capability in pyogp provides a GET and a POST method

    Sample implementations: region.py
    Tests: tests/caps.txt, tests/test_caps.py

    """
    __module__ = __name__

    def __init__(self, name, public_url, restclient=None, settings=None):
        """ initialize the capability """
        if settings != None:
            self.settings = settings
        else:
            from pyogp.lib.base.settings import Settings
            self.settings = Settings()
        if restclient == None:
            self.restclient = StdLibClient()
        else:
            self.restclient = restclient
        self.name = name
        self.public_url = public_url
        return

    def GET(self, custom_headers={}):
        """call this capability, return the parsed result"""
        if self.settings.ENABLE_CAPS_LOGGING:
            logger.debug('%s: GETing %s' % (self.name, self.public_url))
        try:
            response = self.restclient.GET(self.public_url)
        except HTTPError, e:
            if e.code == 404:
                raise ResourceNotFound(self.public_url)
            else:
                raise ResourceError(self.public_url, e.code, e.msg, e.fp.read(), method='GET')

        content_type_charset = response.headers['Content-Type']
        content_type = content_type_charset.split(';')[0]
        if content_type == 'application/llsd+xml':
            deserializer = LLSDDeserializer()
        else:
            raise DeserializerNotFound(content_type)
        data = deserializer.deserialize(response.body)
        if self.settings.LOG_VERBOSE and self.settings.ENABLE_CAPS_LLSD_LOGGING:
            logger.debug('Received the following llsd from %s: %s' % (self.public_url, response.body.strip()))
        if self.settings.ENABLE_CAPS_LOGGING:
            logger.debug('Get of cap %s response is: %s' % (self.public_url, data))
        return data

    def POST(self, payload, custom_headers={}):
        """call this capability, return the parsed result"""
        if self.settings.ENABLE_CAPS_LOGGING:
            logger.debug('Sending to cap %s the following payload: %s' % (self.public_url, payload))
        if type(payload) is ListType:
            serializer = ListLLSDSerializer(payload)
        elif type(payload) is DictType:
            serializer = DictLLSDSerializer(payload)
        else:
            raise DeserializerNotFound(type(payload))
        content_type = serializer.content_type
        serialized_payload = serializer.serialize()
        if self.settings.LOG_VERBOSE and self.settings.ENABLE_CAPS_LLSD_LOGGING:
            logger.debug('Posting the following payload to %s: %s' % (self.public_url, serialized_payload))
        headers = {'Content-type': content_type}
        headers.update(custom_headers)
        try:
            response = self.restclient.POST(self.public_url, serialized_payload, headers=headers)
        except HTTPError, e:
            if e.code == 404:
                raise ResourceNotFound(self.public_url)
            else:
                raise ResourceError(self.public_url, e.code, e.msg, e.fp.read(), method='POST')

        return self._response_handler(response)

    def POST_CUSTOM(self, headers, payload):
        """
        call this capability with custom header and payload, useful for posting
        non-LLSD data such as LSLs or notecards 
        """
        try:
            response = self.restclient.POST(self.public_url, payload, headers=headers)
        except HTTPError, e:
            if e.code == 404:
                raise ResourceNotFound(self.public_url)
            else:
                raise ResourceError(self.public_url, e.code, e.msg, e.fp.read(), method='POST')

        return self._response_handler(response)

    def _response_handler(self, response):
        content_type_charset = response.headers['Content-Type']
        content_type = content_type_charset.split(';')[0]
        pattern = re.compile('<\\?xml\\sversion="1.0"\\s\\?><llsd>.*?</llsd>.*')
        if content_type == 'application/llsd+xml' or content_type == 'application/xml' or content_type == 'text/html' and pattern.match(response.body) != None:
            deserializer = LLSDDeserializer()
        else:
            print response
            raise DeserializerNotFound(content_type)
        data = deserializer.deserialize(response.body)
        if self.settings.ENABLE_CAPS_LLSD_LOGGING:
            logger.debug('Received the following llsd from %s: %s' % (self.public_url, response.body.strip()))
        if self.settings.ENABLE_CAPS_LOGGING:
            logger.debug('Post to cap %s response is: %s' % (self.public_url, data))
        return data

    def __repr__(self):
        return "<Capability '%s' for %s>" % (self.name, self.public_url)


class SeedCapability(Capability):
    """ a seed capability which is able to retrieve other capabilities """
    __module__ = __name__

    def get(self, names=[]):
        """ if this is a seed cap we can retrieve other caps here

        Note: changing post key from 'caps' to 'capabilities' for OGP spec updates in Draft 3
        see http://wiki.secondlife.com/wiki/OGP_Base_Draft_3#Seed_Capability_.28Resource_Class.29
        """
        payload = {'capabilities': names}
        parsed_result = self.POST(payload)['capabilities']
        caps = {}
        for name in names:
            caps[name] = Capability(name, parsed_result[name], self.restclient)

        return caps

    def __repr__(self):
        return '<SeedCapability for %s>' % self.public_url