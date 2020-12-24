# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pyogp/apps/viewer_proxy/lib/caps_proxy.py
# Compiled at: 2010-01-09 02:01:31
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
from logging import getLogger
from webob import Request, Response
from llbase import llsd
from eventlet import util
util.wrap_socket_with_coroutine_socket()
from pyogp.lib.base.datatypes import UUID
from pyogp.lib.base.event_queue import EventQueueClient
from pyogp.lib.base.exc import DataParsingError, HTTPError
logger = getLogger('pyogp.lib.base.caps_proxy')

class CapabilitiesProxy(object):
    """ an application class for wsgiref.simple_server which handles 
    proxyied http requests and responses for capabilities """

    def __init__(self, seed_cap_url, proxy_host_ip, proxy_host_port, message_handler=None, restclient=None):
        self.seed_cap_url = seed_cap_url
        self.proxy_host_ip = proxy_host_ip
        self.proxy_host_port = proxy_host_port
        if message_handler != None:
            self.message_handler = message_handler
        else:
            from pyogp.lib.base.message.message_handler import MessageHandler
            self.message_handler = MessageHandler()
        if restclient == None:
            from pyogp.lib.base.network.stdlib_client import StdLibClient
            self.restclient = StdLibClient()
        else:
            self.restclient = restclient
        self.proxy_map = {}
        self.capability_map = {}
        self.event_queue_client = EventQueueClient()
        self.event_queue_url = None
        self.add_proxy(self.seed_cap_url, 'seed_capability')
        logger.info('Initialized the CapabilitiesProxy for %s' % self.seed_cap_url)
        return

    def add_proxy(self, url, capname):
        """ adds the url and it's proxy, and the proxy and it's url"""
        try:
            test = self.proxy_map[url]
        except KeyError:
            uuid = str(UUID().random())
            self.proxy_map[url] = uuid
            self.proxy_map[uuid] = url
            self.capability_map[url] = capname

        return uuid

    def remove_proxy(self, proxied):
        """ removes the url and it's proxy, and the proxy and it's url"""
        val = self.proxy_map[proxied]
        try:
            del self.proxy_map[proxied]
        except KeyError:
            pass

        try:
            del self.proxy_map[val]
            del self.capability_map[val]
        except KeyError:
            pass

    def swap_cap_urls(self, cap_map):
        """ takes the response to a seed_cap request for cap urls
        and maps proxy urls in place of the ones for the sim 
        """
        for cap in cap_map:
            if cap == 'EventQueueGet':
                self.event_queue_url = cap_map[cap]
            cap_proxy_uuid = self.add_proxy(cap_map[cap], cap)
            cap_map[cap] = 'http://%s:%s/%s' % (self.proxy_host_ip,
             self.proxy_host_port,
             cap_proxy_uuid)
            self.capability_map[cap_map[cap]] = cap

        return cap_map

    def __call__(self, environ, start_response):
        """ handle a specific cap request and response using webob objects"""
        self.environ = environ
        self.start = start_response
        self.request = Request(environ)
        self.response = Response()
        logger.info('Calling cap %s (%s) via %s with body of: %s' % (
         self.capability_map[self.proxy_map[self.request.path[1:]]],
         self.proxy_map[self.request.path[1:]],
         self.request.method,
         self.request.body))
        try:
            if self.request.method == 'GET':
                proxy_response = self.restclient.GET(self.proxy_map[self.request.path[1:]])
            elif self.request.method == 'POST':
                proxy_response = self.restclient.POST(self.proxy_map[self.request.path[1:]], self.request.body)
            logger.info('Cap %s (%s) responded with status %s and body of: %s' % (
             self.capability_map[self.proxy_map[self.request.path[1:]]],
             self.proxy_map[self.request.path[1:]],
             proxy_response.status,
             proxy_response.body))
            status = proxy_response.status
            if self.proxy_map[self.request.path[1:]] == self.seed_cap_url:
                cap_map = self.swap_cap_urls(llsd.parse(proxy_response.body))
                data = llsd.format_xml(cap_map)
            elif self.proxy_map[self.request.path[1:]] == self.event_queue_url:
                self.event_queue_client._parse_result(llsd.parse(proxy_response.body))
                data = proxy_response.body
            else:
                data = proxy_response.body
        except HTTPError, error:
            status = error.code
            data = error.msg

        return self.send_response(status, data)

    def send_response(self, status, body=''):
        """ send the response back to the caller """
        logger.debug('Sending cap response to viewer: Status:%s Body:%s' % (status, body))
        self.response.status = status
        self.response.body = body
        return self.response(self.environ, self.start)