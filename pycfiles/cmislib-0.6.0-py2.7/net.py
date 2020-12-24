# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/cmislib/net.py
# Compiled at: 2016-12-29 12:13:05
"""
Module that takes care of network communications for cmislib. It does
not know anything about CMIS or do anything special with regard to the
response it receives.
"""
from urllib import urlencode
import logging, httplib2

class RESTService(object):
    """
    Generic service for interacting with an HTTP end point. Sets headers
    such as the USER_AGENT and builds the basic auth handler.
    """

    def __init__(self):
        self.user_agent = 'cmislib/%s +http://chemistry.apache.org/'
        self.logger = logging.getLogger('cmislib.net.RESTService')

    def get(self, url, username=None, password=None, **kwargs):
        """ Makes a get request to the URL specified."""
        headers = {}
        if kwargs:
            if 'headers' in kwargs:
                headers = kwargs['headers']
                del kwargs['headers']
                self.logger.debug('Headers passed in: %s', headers)
            if url.find('?') >= 0:
                url = url + '&' + urlencode(kwargs)
            else:
                url = url + '?' + urlencode(kwargs)
        self.logger.debug('About to do a GET on:' + url)
        h = httplib2.Http()
        h.add_credentials(username, password)
        headers['User-Agent'] = self.user_agent
        return h.request(url, method='GET', headers=headers)

    def delete(self, url, username=None, password=None, **kwargs):
        """ Makes a delete request to the URL specified. """
        headers = {}
        if kwargs:
            if 'headers' in kwargs:
                headers = kwargs['headers']
                del kwargs['headers']
                self.logger.debug('Headers passed in: %s', headers)
            if url.find('?') >= 0:
                url = url + '&' + urlencode(kwargs)
            else:
                url = url + '?' + urlencode(kwargs)
        self.logger.debug('About to do a DELETE on:' + url)
        h = httplib2.Http()
        h.add_credentials(username, password)
        headers['User-Agent'] = self.user_agent
        return h.request(url, method='DELETE', headers=headers)

    def put(self, url, payload, contentType, username=None, password=None, **kwargs):
        """
        Makes a PUT request to the URL specified and includes the payload
        that gets passed in. The content type header gets set to the
        specified content type.
        """
        headers = {}
        if kwargs:
            if 'headers' in kwargs:
                headers = kwargs['headers']
                del kwargs['headers']
                self.logger.debug('Headers passed in: %s', headers)
            if url.find('?') >= 0:
                url = url + '&' + urlencode(kwargs)
            else:
                url = url + '?' + urlencode(kwargs)
        self.logger.debug('About to do a PUT on:' + url)
        h = httplib2.Http()
        h.add_credentials(username, password)
        headers['User-Agent'] = self.user_agent
        if contentType is not None:
            headers['Content-Type'] = contentType
        return h.request(url, body=payload, method='PUT', headers=headers)

    def post(self, url, payload, contentType, username=None, password=None, **kwargs):
        """
        Makes a POST request to the URL specified and posts the payload
        that gets passed in. The content type header gets set to the
        specified content type.
        """
        headers = {}
        if kwargs:
            if 'headers' in kwargs:
                headers = kwargs['headers']
                del kwargs['headers']
                self.logger.debug('Headers passed in: %s', headers)
            if url.find('?') >= 0:
                url = url + '&' + urlencode(kwargs)
            else:
                url = url + '?' + urlencode(kwargs)
        self.logger.debug('About to do a POST on:' + url)
        h = httplib2.Http()
        h.add_credentials(username, password)
        headers['User-Agent'] = self.user_agent
        if contentType is not None:
            headers['Content-Type'] = contentType
        return h.request(url, body=payload, method='POST', headers=headers)