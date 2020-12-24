# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/asyncluster/ndm/main.py
# Compiled at: 2007-11-29 13:43:34
"""
The main module of the NDM application. Installs a PyQt4 QApplication() object
into Twisted's qtreactor().
"""
import os
from twisted.internet import defer
CONFIG_PATH = '/etc/asyncluster.conf'

class BaseManager(object):
    """
    I am a base class for the node client, GUI or console.

    @ivar d: A deferred that fires when the client connects to the
      AsynCluster server.

    @ivar config: A L{configobj} config object loaded from the config file.
    
    """
    __module__ = __name__

    def __init__(self):
        from twisted.internet import reactor
        self.reactor = reactor
        self.reactor.callWhenRunning(self.startup)
        self.reactor.run()

    def gotConnected(self, sessionMgr):
        """
        Connected callback for console clients.
        """
        self.sessionMgr = sessionMgr

    def startup(self):
        import configobj, client
        self.config = configobj.ConfigObj(CONFIG_PATH)
        self.client = client.Client(self)
        self.activeUser = None
        self.client.connect().addCallback(self.gotConnected)
        return

    def shutdown(self):
        d = self.client.disconnect()
        d.addCallback(lambda _: self.reactor.stop())
        return d

    def sessionBegin(self, user, password):
        """
        For all clients, requests a session for the specified I{user},
        authenticated with the supplied I{password}.
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
        For all clients, updates the session.
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
        For all clients, ends the session.
        """
        self.activeUser = None
        if callServer:
            return self.sessionMgr.callRemote('end')
        return defer.succeed(None)


class GuiManager(BaseManager):
    """
    """
    __module__ = __name__

    def __init__(self):
        from twisted_goodies.qtwisted import qt4reactor
        from PyQt4.QtGui import QApplication
        self.app = QApplication([])
        qt4reactor.install(self.app)
        from twisted.internet import reactor
        self.reactor = reactor
        import gui
        self.gui = gui
        self.reactor.callWhenRunning(self.startup)
        self.reactor.run()

    def gotConnected(self, sessionMgr):
        """
        Connected callback for GUI clients.
        """
        self.sessionMgr = sessionMgr
        self.loginWindow = self.gui.LoginWindow(self)

    def sessionEnd(self, callServer=True):
        """
        Ends the session for GUI clients.
        """
        self.loginWindow.show()
        self.loginWindow.repaint()
        if hasattr(self, 'sessionWindow'):
            self.sessionWindow.wmStop()
            self.sessionWindow.close()
            del self.sessionWindow
        return BaseManager.sessionEnd(self, callServer)


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-g', '--gui', action='store_true', dest='gui', help='Run the NDM application in a fixed-sized, unmanaged window')
    (opts, args) = parser.parse_args()
    if opts.gui:
        GuiManager()
    else:
        BaseManager()