# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cptsoul/mainwindow/mainstatus.py
# Compiled at: 2013-09-10 02:43:40
import gtk
from cptsoul.common import CptCommon

class MainStatus(gtk.Statusbar, CptCommon):

    def __init__(self):
        super(MainStatus, self).__init__()
        self.push(0, 'Welcome')
        self.manager.connect('logged', self.loggedEvent)
        self.manager.connect('reconnecting', self.reconnectingEvent)
        self.manager.connect('disconnected', self.disconnectedEvent)
        self.manager.connect('connecting', self.connectingEvent)

    def connectingEvent(self, widget):
        self.push(0, 'Connecting...')

    def loggedEvent(self, widget):
        self.push(0, 'Connected')

    def reconnectingEvent(self, widget):
        self.push(0, 'Reconnecting...')

    def disconnectedEvent(self, widget):
        self.push(0, 'Disconnected')