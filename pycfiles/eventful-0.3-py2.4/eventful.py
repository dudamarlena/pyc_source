# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/eventful.py
# Compiled at: 2007-08-06 15:09:47
"""
eventful

A Python interface to the Eventful API.

"""
__author__ = "Edward O'Connor <ted@eventful.com>"
__copyright__ = 'Copyright 2005, 2006 Eventful Inc.'
__license__ = 'MIT'
import md5, urllib, httplib2, simplejson
__all__ = [
 'APIError', 'API']

class APIError(Exception):
    __module__ = __name__


class API:
    __module__ = __name__

    def __init__(self, app_key, server='api.eventful.com', cache=None):
        """Create a new Eventful API client instance.
If you don't have an application key, you can request one:
    http://api.eventful.com/keys/"""
        self.app_key = app_key
        self.server = server
        self.http = httplib2.Http(cache)

    def call(self, method, **args):
        """Call the Eventful API's METHOD with ARGS."""
        args['app_key'] = self.app_key
        if hasattr(self, 'user_key'):
            args['user'] = self.user
            args['user_key'] = self.user_key
        args = urllib.urlencode(args)
        url = 'http://%s/json/%s?%s' % (self.server, method, args)
        (response, content) = self.http.request(url, 'GET')
        status = int(response['status'])
        if status == 200:
            try:
                return simplejson.loads(content)
            except ValueError:
                raise APIError('Unable to parse API response!')

        elif status == 404:
            raise APIError('Method not found: %s' % method)
        else:
            raise APIError('Non-200 HTTP response status: %s' % response['status'])

    def login(self, user, password):
        """Login to the Eventful API as USER with PASSWORD."""
        nonce = self.call('/users/login')['nonce']
        response = md5.new(nonce + ':' + md5.new(password).hexdigest()).hexdigest()
        login = self.call('/users/login', user=user, nonce=nonce, response=response)
        self.user_key = login['user_key']
        self.user = user
        return user