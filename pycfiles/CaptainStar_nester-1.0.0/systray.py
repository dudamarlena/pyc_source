# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cptsoul/systray.py
# Compiled at: 2013-09-10 02:43:40
import gtk
from cptsoul import icons
from cptsoul.common import CptCommon
from cptsoul.notify import Notifier

class Systray(gtk.StatusIcon, CptCommon):

    def __init__(self):
        super(Systray, self).__init__()
        self._reconnecting = False
        self._notifier = Notifier()
        self.set_from_pixbuf(icons.shield)
        self.set_properties(tooltip_text='CaptainSoul', visible=True)
        self.connect('activate', self.mainWindow.showHideEvent)
        self.manager.connect('msg', self.msgEvent)
        self.manager.connect('logged', self.loggedEvent)
        self.manager.connect('reconnecting', self.reconnectingEvent)

    def msgEvent(self, widget, info, msg, dests):
        self._notifier.notify('CaptainSoul - New message from %s' % info.login, msg, 'dialog-information')

    def loggedEvent(self, widget):
        self._reconnecting = False
        self._notifier.notify('CaptainSoul', 'Connected', 'dialog-ok')

    def reconnectingEvent(self, widget):
        if not self._reconnecting:
            self._notifier.notify('CaptainSoul', 'Connection lost, reconnecting', 'dialog-warning')
            self._reconnecting = True