# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cptsoul/chatwindow/chatstatus.py
# Compiled at: 2013-09-10 02:43:40
import gtk
from cptsoul.common import CptCommon

class ChatStatus(gtk.Statusbar, CptCommon):

    def __init__(self, login):
        super(ChatStatus, self).__init__()
        self.connect('destroy', self.destroyEvent)
        self._connections = [
         self.manager.connect('is-typing', self.isTypingEvent, login),
         self.manager.connect('cancel-typing', self.cancelTypingEvent, login)]

    def isTypingEvent(self, widget, info, login):
        if info.login == login:
            self.push(0, 'Is typing...')

    def cancelTypingEvent(self, widget, info, login):
        if info.login == login:
            self.remove_all(0)

    def destroyEvent(self, widget):
        for co in self._connections:
            self.manager.disconnect(co)