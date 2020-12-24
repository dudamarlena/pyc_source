# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/asyncluster/ndm/node.py
# Compiled at: 2008-02-23 09:49:50
"""
The main module for node workers.

"""
CONFIG_PATH = '/etc/asyncluster.conf'

class Manager(object):
    """
    I manage a node client. Instantiate me with I{headless} set C{True} if
    there will be no GUI for user logins or display management.
    
    @ivar config: A L{configobj} config object loaded from the config file.
    
    """
    __module__ = __name__

    def __init__(self, headless=False, duration=None):
        import configobj
        self.config = configobj.ConfigObj(CONFIG_PATH)
        if headless:
            self.gui = None
        else:
            import gui
            self.gui = gui
        from twisted.internet import reactor
        reactor.callWhenRunning(self.startup)
        if isinstance(duration, (float, int)):
            reactor.callLater(float(duration), reactor.stop)
        reactor.run()
        return

    def startup(self):
        """
        Instantiates a session-capable client and connects it to the server.
        """

        def gotSessionMgr(sessionMgr):
            self.sessionMgr = sessionMgr
            if self.gui:
                self.loginWindow = self.gui.LoginWindow(self)

        import client
        self.client = client.Client(self, session=True)
        d = self.client.connect()
        d.addCallback(lambda p: p.callRemote('getSessionManager'))
        d.addCallback(gotSessionMgr)
        return d

    def sessionBegin(self, user, password):
        """
        Requests a session for the specified I{user}, authenticated with the
        supplied I{password}.
        """

        def gotSessionAnswer(approved):
            if approved:
                if hasattr(self, 'loginWindow'):
                    self.loginWindow.hide()
                    self.sessionWindow = self.gui.SessionWindow(self, user)
                    self.sessionWindow.show()
                self.activeUser = user
                d = self.sessionMgr.callRemote('timeLeft')
                d.addCallback(self.sessionUpdate)
                return d

        d = self.sessionMgr.callRemote('begin', user, password)
        d.addCallback(gotSessionAnswer)
        return d

    def sessionUpdate(self, hoursLeft):
        """
        Updates the session.
        """
        if self.activeUser is None:
            return
        if hoursLeft > 0.0:
            if hasattr(self, 'sessionWindow'):
                self.sessionWindow.update(hoursLeft)
        else:
            self.sessionEnd(callServer=False)
        return

    def sessionEnd(self, callServer=True):
        """
        Ends the session, returning a deferred that fires when I'm ready for a
        new session.
        """
        if hasattr(self, 'loginWindow'):
            self.loginWindow.show()
            self.loginWindow.repaint()
        if hasattr(self, 'sessionWindow'):
            self.sessionWindow.wmStop()
            self.sessionWindow.close()
            del self.sessionWindow
        self.activeUser = None
        if callServer:
            return self.sessionMgr.callRemote('end')
        from twisted.internet import defer
        return defer.succeed(None)


def run():
    Manager()


def runHeadless(duration=None):
    Manager(headless=True, duration=duration)