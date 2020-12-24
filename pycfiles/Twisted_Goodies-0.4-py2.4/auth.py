# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twisted_goodies/simpleserver/http/auth.py
# Compiled at: 2007-07-25 20:51:21
"""
Provides an authenticated wrapper for C{twisted.web2.iweb.IResource}
implementations.
"""
from zope.interface import Interface, implements
from twisted.cred import portal, checkers
from twisted.web2.auth import digest, basic, wrapper

class IHTTPUser(Interface):
    """From twisted/doc/web2/examples/auth/credsetup.py"""
    __module__ = __name__


class HTTPUser(object):
    """From twisted/doc/web2/examples/auth/credsetup.py"""
    __module__ = __name__
    implements(IHTTPUser)


class HTTPAuthRealm(object):
    """From twisted/doc/web2/examples/auth/credsetup.py"""
    __module__ = __name__
    implements(portal.IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        if IHTTPUser in interfaces:
            return (
             IHTTPUser, HTTPUser())
        raise NotImplementedError('Only IHTTPUser interface is supported')


class AuthResource(wrapper.HTTPAuthResource):
    """
    Instantiate me with a reference to a C{twisted.web2.iweb.IResource}
    provider and the path of a user:password file and I'll provide secure
    access to the resource.
    """
    __module__ = __name__
    addSlash = False
    authSpecs = {}

    def __init__(self, protectedResource, passwd, realmName='default'):
        self.cacheKey = (passwd, realmName)
        if self.cacheKey not in self.authSpecs:
            credFactories = (
             basic.BasicCredentialFactory(realmName), digest.DigestCredentialFactory('md5', realmName))
            thisPortal = portal.Portal(HTTPAuthRealm())
            thisPortal.registerChecker(checkers.FilePasswordDB(passwd))
            specs = (credFactories, thisPortal)
            self.authSpecs[self.cacheKey] = specs
        specs = (
         protectedResource,) + self.authSpecs[self.cacheKey] + (IHTTPUser,)
        print 'AUTH', specs, passwd
        wrapper.HTTPAuthResource.__init__(self, *specs)