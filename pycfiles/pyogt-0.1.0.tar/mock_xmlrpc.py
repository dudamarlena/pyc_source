# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/tests/mock_xmlrpc.py
# Compiled at: 2010-02-09 00:00:15
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
import urlparse
from pyogp.lib.base.exc import HTTPError
from webob import Request, Response
from webob.exc import HTTPException, HTTPExceptionMiddleware
from cStringIO import StringIO

class MockXMLRPC(object):
    """implement a REST client on top of urllib2"""
    __module__ = __name__

    def __init__(self, wsgi_app, loginuri):
        self.app = wsgi_app
        self.loginuri = loginuri

    def login_to_simulator(self, data, headers={}):
        """ mimic logging in via xmlrpc """
        request = Request.blank(self.loginuri)
        request.body = str(data)
        request.method = 'login_to_simulator'
        response = request.get_response(self.app)
        if not response.status.startswith('2'):
            parts = response.status.split(' ')
            msg = (' ').join(parts[1:])
            raise HTTPError(response.status_int, msg, StringIO(response.body))
        return self.send_response(response)

    def mock_transform(self, data, headers={}):
        """ GET a resource """
        request = Request.blank(self.loginuri)
        request.body = str(data)
        request.method = 'mock_transform'
        response = request.get_response(self.app)
        if not response.status.startswith('2'):
            parts = response.status.split(' ')
            msg = (' ').join(parts[1:])
            raise HTTPError(response.status_int, msg, StringIO(response.body))
        return self.send_response(response)

    def send_response(self, response):
        result = response.body.split()
        mydict = {}
        counter = 0
        key = None
        value = None
        for item in result:
            counter += 1
            if counter % 2:
                key = item
            else:
                mydict[key] = item

        return mydict

    def __getattr__(self, attribute):
        return getattr(self, attribute)

    def __repr__(self):
        """ return a representation of itself """
        return 'Restclient is MockupClient using webob and wsgi for %s' % self.app