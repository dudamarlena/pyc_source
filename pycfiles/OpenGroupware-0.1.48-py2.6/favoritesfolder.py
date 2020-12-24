# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/favoritesfolder.py
# Compiled at: 2012-10-12 07:02:39
import datetime, pprint, hashlib
from coils.net import DAVFolder, OmphalosCollection, OmphalosObject, StaticObject, EmptyFolder
from contactsfolder import ContactsFolder

class FavoritesFolder(DAVFolder):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def get_property_webdav_owner(self):
        return ('<href>/dav/Contacts/{0}.vcf</href>').format(self.context.account_id)

    def _load_contents(self):
        self.insert_child('Contacts', ContactsFolder(self, 'Contacts', context=self.context, request=self.request))
        self.insert_child('Enterprises', EmptyFolder(self, 'Enterprises', context=self.context, request=self.request))
        return True

    def object_for_keys(self, name, auto_load_enabled=True, is_webdav=False):
        if auto_load_enabled:
            self.load_contents()
        if self.is_loaded:
            result = self.get_child(name)
            if result is not None:
                return result
        self.no_such_path()
        return