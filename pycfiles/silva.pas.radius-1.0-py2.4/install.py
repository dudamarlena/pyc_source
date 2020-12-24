# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.freebsd-7.1-PRERELEASE-i386/egg/silva/pas/radius/install.py
# Compiled at: 2008-11-20 12:49:45
from zope.interface import alsoProvides, noLongerProvides
from Products.PluggableAuthService.interfaces.plugins import *
from silva.pas.base.interfaces import IPASMemberService
from interfaces import IRaduisAware

def install(root):
    """Installation method for OpenID support
    """
    assert IPASMemberService.providedBy(root.service_members)
    registerPASPlugins(root.acl_users)
    alsoProvides(root.service_members, IRaduisAware)


def uninstall(root):
    """Uninstall OpenID support
    """
    assert IPASMemberService.providedBy(root.service_members)
    unregisterPASPlugins(root.acl_users)
    noLongerProvides(root.service_members, IRaduisAware)


def is_installed(root):
    return IRaduisAware.providedBy(root.service_members)


def registerPASPlugins(pas):
    """Register new PAS plugins.
    """
    pas.manage_addProduct['plone.session'].manage_addSessionPlugin('session')
    pas.manage_addProduct['silva.pas.membership'].manage_addMembershipPlugin('members')
    if getattr(pas, 'raduis', None) is None:
        pas.manage_addProduct['silva.pas.radius'].manage_addRadiusPlugin('radius')
    plugins = pas.plugins
    plugins.activatePlugin(IExtractionPlugin, 'session')
    plugins.movePluginsUp(IExtractionPlugin, ['session'])
    plugins.activatePlugin(IAuthenticationPlugin, 'session')
    plugins.movePluginsUp(IAuthenticationPlugin, ['session'])
    plugins.movePluginsUp(IAuthenticationPlugin, ['session'])
    plugins.deactivatePlugin(ICredentialsResetPlugin, 'cookie_auth')
    plugins.activatePlugin(ICredentialsResetPlugin, 'session')
    plugins.deactivatePlugin(ICredentialsUpdatePlugin, 'cookie_auth')
    plugins.activatePlugin(ICredentialsUpdatePlugin, 'session')
    plugins.activatePlugin(IAuthenticationPlugin, 'radius')
    plugins.movePluginsUp(IAuthenticationPlugin, ['radius'])
    plugins.movePluginsUp(IAuthenticationPlugin, ['radius'])
    plugins.activatePlugin(IUserEnumerationPlugin, 'members')
    plugins.movePluginsUp(IUserEnumerationPlugin, ['members'])
    plugins.movePluginsUp(IUserEnumerationPlugin, ['members'])
    return


def unregisterPASPlugins(pas):
    """Remove PAS plugins.
    """
    pas.manage_delObjects(['session', 'members'])
    plugins = pas.plugins
    plugins.deactivatePlugin(IAuthenticationPlugin, 'radius')
    plugins.activatePlugin(ICredentialsResetPlugin, 'cookie_auth')
    plugins.activatePlugin(ICredentialsUpdatePlugin, 'cookie_auth')


if __name__ == '__main__':
    print "This module is not an installer. You don't have to run it."