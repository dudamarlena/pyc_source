# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cptsoul/chatwindow/chatview.py
# Compiled at: 2014-01-13 06:59:05
import re, webbrowser
from time import localtime, strftime
import gtk
from cptsoul.htmltextview import HtmlTextView
from cptsoul.common import CptCommon

class ChatView(gtk.ScrolledWindow, CptCommon):
    http_regex = re.compile("(https?://[\\w\\-\\.~\\:/\\?#\\[\\]@!$&'\\(\\)\\*\\+,;=%]+)")

    def __init__(self, entry, login, msg=None):
        super(ChatView, self).__init__()
        self.set_properties(border_width=0, shadow_type=gtk.SHADOW_ETCHED_IN, hscrollbar_policy=gtk.POLICY_NEVER, vscrollbar_policy=gtk.POLICY_AUTOMATIC)
        self._buffer = ''
        self._view = None
        self._createUi(entry)
        self.connect('destroy', self.destroyEvent)
        self._connections = [
         self.manager.connect('msg', self.msgEvent, login),
         self.manager.connect('send-msg', self.sendMsgEvent, login)]
        if msg is not None:
            self.printMsg(login, msg)
        return

    def _createUi(self, entry):
        self._view = HtmlTextView()
        self._view.connect('url-clicked', self.openLink)
        self._view.connect('focus-in-event', self.focusInEvent, entry)
        self._view.connect('size-allocate', self.scrollView)
        self.add(self._view)

    def focusInEvent(self, widget, event, entry):
        entry.grab_focus()

    def scrollView(self, widget, alloc):
        adj = self.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())

    def printMsg(self, login, msg):
        t = strftime('%H:%M:%S', localtime())
        self._buffer += '(%s) <span style="font-weight: bold">[%s]</span> : ' % (t, login)
        changes = [
         ('&', '&amp;'),
         ('<', '&lt;'),
         ('>', '&gt;'),
         ('\t', '&emsp;'),
         ('\n', '<br/>')]
        for orig, new in changes:
            msg = re.sub(orig, new, msg)

        self._buffer += self.http_regex.sub('<a href="\\1">\\1</a>', msg)
        self._buffer += '<br/>'
        self._view.set_html('<body>%s</body>' % self._buffer)

    def msgEvent(self, widget, info, msg, dests, login):
        if login == info.login:
            self.printMsg(login, msg)

    def sendMsgEvent(self, widget, msg, dests, login):
        if login in dests:
            self.printMsg('Me', msg)

    def destroyEvent(self, widget):
        for co in self._connections:
            self.manager.disconnect(co)

    def openLink(self, widget, url, type_):
        webbrowser.open_new_tab(url)
        return True