# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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