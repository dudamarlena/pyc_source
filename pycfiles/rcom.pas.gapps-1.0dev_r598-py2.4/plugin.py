# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rcom/pas/gapps/plugin.py
# Compiled at: 2008-07-07 23:44:16
"""Class: GappsHelper
"""
import gdata.base.service
from OFS.Cache import Cacheable
from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin, ICredentialsResetPlugin, IUserAdderPlugin, IRoleAssignerPlugin
from Products.PluggableAuthService.utils import classImplements
import interface, plugins

class GappsHelper(BasePlugin, Cacheable):
    """Multi-plugin

    """
    __module__ = __name__
    meta_type = 'GApps Authentication Helper'
    security = ClassSecurityInfo()

    def __init__(self, id, title=None):
        self._setId(id)
        self.title = title

    security.declarePrivate('authenticateCredentials')

    def authenticateCredentials(self, credentials):
        """ See IAuthenticationPlugin.

        o We expect the credentials to be those returned by
          ILoginPasswordExtractionPlugin.
        """
        login = credentials.get('login')
        password = credentials.get('password')
        if login is None or password is None:
            return
        ga = gdata.base.service.GBaseService(login, password)
        try:
            ga.ProgrammaticLogin()
            if self._getPAS().getUserById(login) is None:
                self.makeMember(login, password)
        except gdata.service.BadAuthentication, e:
            return
        except Exception, e:
            return

        return (
         login, login)

    def makeMember(self, loginname, password):
        """Make a user with id `userId`, and assign him the Member role."""
        userAdders = self.plugins.listPlugins(IUserAdderPlugin)
        if not userAdders:
            raise NotImplementedError('I wanted to make a new user, but there are no PAS plugins active that can make users.')
        roleAssigners = self.plugins.listPlugins(IRoleAssignerPlugin)
        if not roleAssigners:
            raise NotImplementedError('I wanted to make a new user and give him the Member role, but there are no PAS plugins active that assign roles to users.')
        user = None
        for (_, curAdder) in userAdders:
            if curAdder.doAddUser(loginname, password):
                user = self._getPAS().getUser(loginname)
                break

        for (curAssignerId, curAssigner) in roleAssigners:
            try:
                curAssigner.doAssignRoleToPrincipal(user.getId(), 'Member')
            except _SWALLOWABLE_PLUGIN_EXCEPTIONS:
                logger.debug('RoleAssigner %s error' % curAssignerId, exc_info=True)

        return


classImplements(GappsHelper, interface.IGappsHelper)
InitializeClass(GappsHelper)