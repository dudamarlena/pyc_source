# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cptsoul/addcontactwindow.py
# Compiled at: 2014-01-02 09:25:02
import logging, gtk

class AddContactWindow(gtk.Dialog):

    def __init__(self):
        super(AddContactWindow, self).__init__(title='CaptainSoul - Add contact')
        logging.debug('Create Window')
        self.set_properties(resizable=False)
        self._entry = None
        self._createUi()
        self.show_all()
        return

    def activateEvent(self, wid):
        self.response(gtk.RESPONSE_OK)

    def getLogin(self):
        return self._entry.get_text().strip()

    def _createUi(self):
        self._entry = gtk.Entry()
        self._entry.connect('activate', self.activateEvent)
        self.vbox.pack_start(self._entry, True, True, 0)
        self.add_buttons('Add', gtk.RESPONSE_OK, 'Cancel', gtk.RESPONSE_CANCEL)