# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/files/addressbooks.py
# Compiled at: 2012-10-12 07:02:39
import hashlib
from coils.core import Contact, Enterprise, CTag
from coils.net import DAVFolder, DAVObject, EmptyFolder
from csvobject import CSVObject

class AddressBooksFolder(DAVFolder):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def _load_contents(self):
        self.insert_child('FavoriteContacts.txt', None)
        self.insert_child('AllContacts.txt', None)
        return True

    def _get_ctag_for_entity(self, entity):
        """ Return a ctag appropriate for this object.
            Actual WebDAV objects should override this method """
        db = self.context.db_session()
        query = db.query(CTag).filter(CTag.entity == entity)
        ctags = query.all()
        if len(ctags) == 0:
            return
        else:
            query = None
            return ctags[0].ctag

    def _ctag_for_enumeration(self, enumeration):
        m = hashlib.md5()
        for entry in enumeration:
            m.update(('{0}:{1}').format(entry[0], entry[1]))

        return m.hexdigest()

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if name == 'FavoriteContacts.txt':
            contents = self.context.run_command('contact::get-favorite', properties=[Contact.object_id, Contact.version])
            contents.sort()
            ctag = self._ctag_for_enumeration(contents)
            return CSVObject(self, name, command='contact::get-favorite', ctag=ctag, context=self.context, request=self.request)
        if name == 'AllContacts.txt':
            ctag = self._get_ctag_for_entity('Person')
            return CSVObject(self, name, command='contact::list', ctag=ctag, context=self.context, request=self.request)
        self.no_such_path()