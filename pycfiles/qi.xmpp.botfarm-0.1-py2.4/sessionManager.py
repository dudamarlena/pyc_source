# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/xmpp/botfarm/sessionManager.py
# Compiled at: 2008-08-11 09:44:36
from twisted.internet import interfaces, defer, reactor
from qi.xmpp.botfarm.session import Session
from qi.xmpp.botfarm.logutil import LogEvent, INFO, WARN, ERROR
import qi.xmpp.client.ns as ns, qi.xmpp.botfarm.config as config
from qi.xmpp.client.avatar import getDefaultAvatarData, Avatar, AvatarStorage
from qi.xmpp.admin.admin import AdminSession

class SessionManager:
    """
        """
    __module__ = __name__

    def __init__(self):
        """
                """
        self.sessions = dict()
        self.connections = dict()
        self.avatarStorage = AvatarStorage()
        self.defaultAvatar = Avatar(getDefaultAvatarData(config.defaultAvatar), self.avatarStorage)

    def loadBot(self, botid, botpass, persistent=False):
        if self.sessions.has_key(botid):
            return True
        s = Session(botid, self, self.defaultAvatar, persistent)
        s.disco.addIdentity(category='client', ctype='web', name=config.app_name)
        s.disco.addFeature(ns.NS_DISCO_INFO, s.disco.onDiscoInfo)
        s.disco.addFeature(ns.NS_IQROSTER, s.roster.onRosterUpdate)
        s.disco.addFeature(ns.NS_IQVERSION, s.disco.onApplicationVersion)
        s.disco.addFeature(ns.NS_XVCARDUPDATE, None)
        s.disco.addFeature(ns.NS_VCARDTEMP, None)
        s.disco.addFeature(ns.NS_SI, s.filetransfer.onStreamInitiation)
        s.disco.addFeature(ns.NS_FT, None)
        s.disco.addFeature(ns.NS_S5B, s.filetransfer.onInitSOCKS5)
        s.disco.addFeature(ns.NS_PING, s.pingpong.onPing)
        d = s.login(botpass)
        self.sessions[botid] = s
        self.connections[botid] = reactor.connectTCP(s.jserver, 5222, s.jfactory)

        def onLoginResult(authenticated):
            if not authenticated:
                self.delSession(botid)
            return authenticated

        d.addCallback(onLoginResult)
        return d

    def loadAdminSession(self):
        """
                """
        adminid = ('@').join([config.admin_id, config.server])
        adminpass = config.admin_pass
        s = AdminSession(adminid, self)
        s.disco.addFeature(ns.NS_DISCO_INFO, s.disco.onDiscoInfo)
        d = s.login(adminpass)
        self.sessions[adminid] = s
        self.connections[adminid] = reactor.connectTCP(s.jserver, 5222, s.jfactory)

        def onLoginResult(authenticated):
            if not authenticated:
                LogEvent(ERROR, 'admin session could not be loaded')
            else:
                LogEvent(INFO, 'admin session loaded succesfully')

        d.addCallback(onLoginResult)

    def unloadSessions(self):
        """
                """
        for session in self.sessions.values():
            session.logout()

    def delSession(self, sessionid):
        if self.connections.has_key(sessionid):
            self.connections[sessionid].disconnect()
            del self.connections[sessionid]
            del self.sessions[sessionid]