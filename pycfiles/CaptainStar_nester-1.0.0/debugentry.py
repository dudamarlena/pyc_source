# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cptsoul/debugwindow/debugentry.py
# Compiled at: 2013-09-10 02:43:40
import gtk
from cptsoul.common import CptCommon

class DebugEntry(gtk.Entry, CptCommon):

    def __init__(self):
        super(DebugEntry, self).__init__()
        self.connect('activate', self.activateEvent)

    def activateEvent(self, widget):
        line = widget.get_text()
        if line:
            widget.set_text('')
            self.manager.sendRaw(line)