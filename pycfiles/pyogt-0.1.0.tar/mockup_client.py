# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/tests/mockup_client.py
# Compiled at: 2010-02-09 00:00:15
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
import urlparse
from pyogp.lib.base.exc import HTTPError
from webob import Request, Response
from webob.exc import HTTPException, HTTPExceptionMiddleware
from cStringIO import StringIO

class MockupClient(object):
    """implement a REST client on top of urllib2"""
    __module__ = __name__

    def __init__(self, wsgi_app):
        self.app = wsgi_app

    def strip_url(self, url):
        """remove server/host from the URL"""
        o = urlparse.urlparse(url)
        p = o[2]
        if o[4]:
            p = p + '?' + o[4]
        if o[5]:
            p = p + '#' + o[5]
        return url

    def GET(self, url, headers={}):
        """GET a resource"""
        request = Request.blank(self.strip_url(url))
        request.method = 'GET'
        response = request.get_response(self.app)
        if not response.status.startswith('2'):
            parts = response.status.split(' ')
            msg = (' ').join(parts[1:])
            raise HTTPError(response.status_int, msg, StringIO(response.body))
        return response

    def POST(self, url, data, headers={}):
        """POST data to a resource"""
        request = Request.blank(self.strip_url(url))
        request.body = data
        request.method = 'POST'
        response = request.get_response(self.app)
        if not response.status.startswith('2'):
            parts = response.status.split(' ')
            msg = (' ').join(parts[1:])
            raise HTTPError(response.status_int, msg, StringIO(response.body))
        return response

    def __repr__(self):
        """ return a representation of itself """
        return 'Restclient is MockupClient using webob and wsgi for %s' % self.app