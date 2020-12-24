# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cluebin/googledata.py
# Compiled at: 2008-06-27 12:04:19
from google.appengine.ext import db
from cluebin import paste

class GooglePaste(db.Model, paste.Paste):
    author_name = db.StringProperty()
    language = db.StringProperty()
    paste = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)

    @property
    def pasteid(self):
        return self.key().id()

    @staticmethod
    def kind():
        return 'Paste'


class GooglePasteDataStore(paste.PasteDataStore):

    def get_paste(self, pasteid):
        return GooglePaste.get_by_id(int(pasteid))

    def get_pastes(self):
        return db.GqlQuery('SELECT * FROM Paste ORDER BY date DESC LIMIT 10')

    def gen_paste(self):
        return GooglePaste()

    def save_paste(self, p):
        p.put()