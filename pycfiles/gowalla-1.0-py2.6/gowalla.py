# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/gowalla/gowalla.py
# Compiled at: 2010-05-04 23:04:46
"""A minimalist Python interface for the Gowalla API"""
__author__ = 'Drew Yeaton <drew@sentineldesign.net>'
__version__ = '1.0'
import base64, types, urllib, urllib2
from urllib2 import URLError, HTTPError
import simplejson
URL = 'http://gowalla.com'
CRUD_METHODS = {'create': 'POST', 
   'read': 'GET', 
   'update': 'PUT', 
   'delete': 'DELETE'}

class GowallaException(Exception):
    pass


class GowallaConnectionException(GowallaException):
    pass


class GowallaResourceInvalidException(GowallaException):
    pass


class GowallaUnauthorizedException(GowallaException):
    pass


class GowallaResourceNotFoundException(GowallaException):
    pass


class GowallaMethodNotAllowedException(GowallaException):
    pass


class GowallaNotAcceptableException(GowallaException):
    pass


class GowallaApplicationErrorException(GowallaException):
    pass


class Gowalla(object):
    username = ''
    password = ''
    api_key = ''
    uri = ''
    response = None
    errors = None

    def __init__(self, username='', password='', api_key='', uri=''):
        self.username = username
        self.password = password
        self.api_key = api_key
        self.uri = uri

    def __getattr__(self, k):
        try:
            return object.__getattr__(self, k)
        except AttributeError:
            return Gowalla(self.username, self.password, self.api_key, self.uri + '/' + k)

    def __call__(self, **kwargs):
        urili = self.uri.split('/')
        action = urili.pop()
        try:
            method = CRUD_METHODS[action]
        except KeyError:
            urili.append(action)
            method = 'GET'

        uid = kwargs.pop('id', False)
        if uid:
            urili.insert(2, uid)
        data = None
        args = ''
        if method == 'GET' and kwargs:
            args = '?%s' % urllib.urlencode(kwargs.items())
        url = '%s%s%s' % (URL, ('/').join(urili), args)
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        self._request = urllib2.Request(url=url, data=data)
        self._request.get_method = lambda : method
        self._request.add_header('Accept', 'application/json')
        self._request.add_header('Content-Type', 'application/json')
        self._request.add_header('Authorization', 'Basic %s' % base64.encodestring('%s:%s' % (self.username, self.password))[:-1])
        self._request.add_header('-Gowalla-API-Key', self.api_key)
        try:
            response = opener.open(self._request)
            json_response = response.read()
        except HTTPError, e:
            if e.code in range(200, 205):
                pass
            elif e.code == 400:
                raise GowallaResourceInvalidException(e.read())
            elif e.code == 401:
                raise GowallaUnauthorizedException(e)
            elif e.code == 404:
                raise GowallaResourceNotFoundException(e)
            elif e.code == 405:
                raise GowallaMethodNotAllowedException(e)
            elif e.code == 406:
                raise GowallaNotAcceptableException(e)
            elif e.code == 500:
                raise GowallaApplicationErrorException(e)
            else:
                raise GowallaException(e)
        except URLError, e:
            raise GowallaConnectionException(e)

        self.response = simplejson.loads(json_response)
        return self.response


__all__ = [
 'Gowalla',
 'GowallaException',
 'GowallaConnectionException',
 'GowallaResourceInvalidException',
 'GowallaUnauthorizedException',
 'GowallaResourceNotFoundException',
 'GowallaMethodNotAllowedException',
 'GowallaNotAcceptableException',
 'GowallaApplicationErrorException']