# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/agentdomain.py
# Compiled at: 2010-02-09 00:00:15
"""
Contributors can be viewed at:
http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt 

$LicenseInfo:firstyear=2008&license=apachev2$

Copyright 2009, Linden Research, Inc.

Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
    http://www.apache.org/licenses/LICENSE-2.0
or in 
    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt

$/LicenseInfo$
"""
import urllib2
from logging import getLogger
from llbase import llsd
from pyogp.lib.base.network.stdlib_client import StdLibClient, HTTPError
from pyogp.lib.base.caps import SeedCapability
import pyogp.lib.client.exc
from pyogp.lib.client.settings import Settings
logger = getLogger('pyogp.lib.client.agentdomain')

class AgentDomain(object):
    """an agent domain endpoint"""
    __module__ = __name__

    def __init__(self, uri, restclient=None):
        """ initialize the agent domain endpoint """
        if restclient == None:
            self.restclient = StdLibClient()
        else:
            self.restclient = restclient
        self.settings = Settings()
        self.login_uri = uri
        self.credentials = None
        self.connectedStatus = False
        self.capabilities = {}
        self.agentdomain_caps_list = [
         'rez_avatar/place']
        self._isEventQueueRunning = False
        self.seed_cap = None
        logger.debug('initializing agent domain: %s' % self)
        return

    def login(self, credentials):
        """ login to the agent domain """
        response = self.post_to_loginuri(credentials)
        self.eval_login_response(response)

    def post_to_loginuri(self, credentials):
        """ post to login_uri and return response """
        self.credentials = credentials
        logger.info('Logging in to %s as %s %s' % (self.login_uri, self.credentials.firstname, self.credentials.lastname))
        payload = credentials.serialize()
        content_type = credentials.content_type
        headers = {'Content-Type': content_type}
        try:
            response = self.restclient.POST(self.login_uri, payload, headers=headers)
        except HTTPError, error:
            if error.code == 404:
                raise ResourceNotFound(self.login_uri)
            else:
                raise ResourceError(self.login_uri, error.code, error.msg, error.fp.read(), method='POST')

        return response

    def eval_login_response(self, response):
        """ parse the login uri response """
        seed_cap_url_data = self.parse_login_response(response)
        try:
            seed_cap_url = seed_cap_url_data['agent_seed_capability']
            self.seed_cap = SeedCapability('seed_cap', seed_cap_url, self.restclient)
            self.connectedStatus = True
            logger.info('logged in to %s' % self.login_uri)
        except KeyError:
            raise UserNotAuthorized(self.credentials)

    def parse_login_response(self, response):
        """ parse the login uri response and returns deserialized data """
        data = llsd.parse(response.body)
        logger.debug('deserialized login response body = %s' % data)
        return data

    def place_avatar(self, region_uri, position=[
 117, 73, 21]):
        """ handles the rez_avatar/place cap on the agent domain, populates some initial region attributes """
        if not self.capabilities.has_key('rez_avatar/place'):
            self.capabilities['rez_avatar/place'] = self.seed_cap.get(['rez_avatar/place'])['rez_avatar/place']
        payload = {'public_region_seed_capability': region_uri, 'position': position}
        result = self.capabilities['rez_avatar/place'].POST(payload)
        if result['region_seed_capability'] is None:
            raise UserRezFailed(region)
        else:
            logger.info('Region_uri %s returned a seed_cap of %s' % (region_uri, result['region_seed_capability']))
        logger.debug('Full rez_avatar/place response is: %s' % result)
        return result

    def get_agentdomain_capabilities(self):
        """ queries the region seed cap for capabilities """
        if self.seed_cap == None:
            raise RegionSeedCapNotAvailable("querying for agents's agent domain capabilities")
        else:
            logger.info('Getting caps from agent domain seed cap %s' % self.seed_cap)
            self.capabilities = self.seed_cap.get(self.agentdomain_caps_list)
        return

    def _processEventQueue(self):
        self._isEventQueueRunning = True
        if self.capabilities['event_queue'] == None:
            raise RegionCapNotAvailable('event_queue')
        else:
            while self._isEventQueueRunning:
                data = {}
                api.sleep(self.settings.agentdomain_event_queue_interval)
                result = self.capabilities['event_queue'].POST(data)
                self.last_id = result['id']
                logger.debug('AgentDomain EventQueueGet result: %s' % result)

        return