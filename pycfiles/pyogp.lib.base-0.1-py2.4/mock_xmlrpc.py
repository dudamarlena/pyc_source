# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/tests/mock_xmlrpc.py
# Compiled at: 2010-02-07 17:28:31
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