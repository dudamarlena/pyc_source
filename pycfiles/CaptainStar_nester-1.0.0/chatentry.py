# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cptsoul/chatwindow/chatentry.py
# Compiled at: 2013-09-10 02:43:40
import gtk
from cptsoul.common import CptCommon

class ChatEntry(gtk.TextView, CptCommon):

    def __init__(self, login):
        super(ChatEntry, self).__init__()
        self.set_properties(editable=True, cursor_visible=True, wrap_mode=gtk.WRAP_WORD_CHAR, width_request=100, height_request=40)
        self._typing = False
        self.connect('key-press-event', self.keyPressEvent, login)
        self.get_buffer().connect('changed', self.keyPressEventEnd, login)

    def deleteEvent(self, widget, reason, login):
        if self._typing:
            self._typing = False
            self.manager.sendCancelTyping([login])

    def keyPressEvent(self, widget, event, login):
        if gtk.gdk.keyval_name(event.keyval) in ('Return', 'KP_Enter'):
            buff = self.get_buffer()
            text = buff.get_text(buff.get_start_iter(), buff.get_end_iter(), True)
            if len(text):
                buff.delete(buff.get_start_iter(), buff.get_end_iter())
                self.manager.sendMsg(text, [login])
            return True

    def keyPressEventEnd(self, widget, login):
        buff = self.get_buffer()
        l = len(buff.get_text(buff.get_start_iter(), buff.get_end_iter(), True))
        if not self._typing and l >= 5:
            self.manager.sendStartTyping([login])
            self._typing = True
        elif self._typing and l < 5:
            self.manager.sendCancelTyping([login])
            self._typing = False