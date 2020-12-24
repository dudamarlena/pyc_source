# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/services/auth.py
# Compiled at: 2011-04-22 06:35:42
"""
    Provides a user registry and authentication
 
"""
from twisted.application import internet, service
from twisted.internet import protocol, reactor, defer
from twisted.cred import portal, checkers, credentials, error
from twisted.words.service import WordsRealm, InMemoryWordsRealm
from twisted.words.iwords import IGroup, IUser
from twisted.cred.portal import Portal, IRealm
from zope.interface import implements
from otfbot.lib.user import BotUser
import logging, yaml, hashlib

class YamlWordsRealm(InMemoryWordsRealm):
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (
     credentials.IUsernamePassword,)

    def __init__(self, name, file):
        super(YamlWordsRealm, self).__init__(name)
        self.file = file
        reactor.callInThread(self.load)

    def userFactory(self, name):
        """
            create a new User

            @param name: the name of the new user
            @type name: string
            @returns: a BotUser object
        """
        return BotUser(name)

    def addUser(self, user):
        """
            adds a user to userlist
        """
        super(YamlWordsRealm, self).addUser(user)
        reactor.callInThread(self.save)

    def addGroup(self, group):
        """
            adds a group
        """
        super(YamlWordsRealm, self).addGroup(group)
        reactor.callInThread(self.save)

    def requestAvatarId(self, creds):
        u = self.getUser(unicode(creds.username))
        u.addErrback(error.UnauthorizedLogin)
        u.addCallback(self._checkpw, creds)
        return u

    def requestAvatar(self, avatarId, mind, *interfaces):
        if isinstance(avatarId, str):
            avatarId = avatarId.decode(self._encoding)

        def gotAvatar(avatar):
            for iface in interfaces:
                facet = iface(avatar, None)
                if facet is not None:
                    avatar.loggedIn(self, mind)
                    mind.name = avatarId
                    mind.realm = self
                    mind.avatar = avatar
                    return (
                     iface, facet, self.logoutFactory(avatar, facet))

            raise NotImplementedError(self, interfaces)
            return

        return self.getUser(avatarId).addCallback(gotAvatar)

    def _checkpw(self, user, creds):
        up = credentials.IUsernamePassword(creds)
        if user.checkPasswd(up.password):
            return defer.succeed(user.name)
        else:
            return defer.fail(error.UnauthorizedLogin())

    def save(self):
        """
            writes the userlist to a yaml file
        """
        file = open(self.file, 'w')
        file.write(yaml.dump_all([self.users, self.groups], default_flow_style=False))
        file.close()

    def load(self):
        """
            loads the userlist from a yaml file
        """
        try:
            f = open(self.file, 'r')
            file_h = yaml.load_all(f)
            self.users = file_h.next()
            self.groups = file_h.next()
            f.close()
        except IOError:
            self.users = {}
            self.groups = {}


class botService(service.MultiService, portal.Portal):
    """
        auth service class providing authentification against a userlist
    """
    name = 'auth'

    def __init__(self, root, parent):
        self.root = root
        self.parent = parent
        service.MultiService.__init__(self)
        self.checkers = {}

    def startService(self):
        """
            starts the service and loads the userlist
        """
        print 'auth service started'
        self.config = self.root.getServiceNamed('config')
        self.realm = YamlWordsRealm('userdb', self.config.get('datadir', 'data') + '/userdb.yaml')
        portal.Portal.__init__(self, self.realm)
        self.registerChecker(self.realm, *self.realm.credentialInterfaces)
        service.Service.startService(self)

    def getCheckers(self):
        return self.checkers