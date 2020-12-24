# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/myproxy/ws/server/wsgi/app.py
# Compiled at: 2012-08-01 08:45:50
"""HTTPS proxy to MyProxy server WSGI Application
 
NERC DataGrid Project
"""
__author__ = 'P J Kershaw'
__date__ = '21/05/10'
__copyright__ = '(C) 2010 Science and Technology Facilities Council'
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: $'
from myproxy.ws.server.wsgi.httpbasicauth import HttpBasicAuthMiddleware
from myproxy.ws.server.wsgi.middleware import MyProxyLogonWSMiddleware, MyProxyGetTrustRootsMiddleware

class MyProxyApp(object):
    """HTTP interface to MyProxy logon and get trsut roots.  This interfaces 
    creates a MyProxy client instance with a HTTP Basic Auth based web service 
    interface to pass username/passphrase for MyProxy logon calls.  
    
    This WSGI must be run over HTTPS to ensure confidentiality of 
    username/passphrase credentials.  PKI based verification of requests
    should be done out of band of this app e.g. in other filter middleware or
    Apache SSL configuration.
    """
    PARAM_PREFIX = 'myproxy.'
    LOGON_PARAM_PREFIX = 'logon.'
    GET_TRUSTROOTS_PARAM_PREFIX = 'getTrustRoots.'
    HTTPBASICAUTH_REALM_OPTNAME = 'httpbasicauth.realm'

    @classmethod
    def app_factory(cls, global_conf, prefix=PARAM_PREFIX, **app_conf):
        """Function following Paste app factory signature
        
        @type global_conf: dict        
        @param global_conf: PasteDeploy global configuration dictionary
        @type prefix: basestring
        @param prefix: prefix for configuration items
        @type app_conf: dict        
        @param app_conf: PasteDeploy application specific configuration 
        dictionary
        """
        app = cls()
        logonPrefix = prefix + cls.LOGON_PARAM_PREFIX
        httpBasicAuthMWare = HttpBasicAuthMiddleware.filter_app_factory(app, global_conf, prefix=logonPrefix, **app_conf)
        getTrustRootsPrefix = prefix + cls.GET_TRUSTROOTS_PARAM_PREFIX
        getTrustRootsMWare = MyProxyGetTrustRootsMiddleware.filter_app_factory(httpBasicAuthMWare, global_conf, prefix=getTrustRootsPrefix, **app_conf)
        app = MyProxyLogonWSMiddleware.filter_app_factory(getTrustRootsMWare, global_conf, prefix=prefix, **app_conf)
        httpBasicAuthMWare.authnFuncEnvironKeyName = app.logonFuncEnvironKeyName
        getTrustRootsMWare.clientEnvironKeyName = app.clientEnvironKeyName
        realmOptName = prefix + cls.HTTPBASICAUTH_REALM_OPTNAME
        httpBasicAuthMWare.realm = app_conf[realmOptName]
        return app

    def __call__(self, environ, start_response):
        """Catch case where request path doesn't match mount point for app"""
        status = response = '404 Not Found'
        start_response(status, [
         ('Content-type', 'text/plain'),
         (
          'Content-length', str(len(response)))])
        return [response]