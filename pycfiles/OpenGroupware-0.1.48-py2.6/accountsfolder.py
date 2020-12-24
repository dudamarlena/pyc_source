# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/accountsfolder.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime
from coils.net import DAVObject, DAVFolder
from groupwarefolder import GroupwareFolder

class AccountsFolder(DAVFolder, GroupwareFolder):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def get_property_unknown_getctag(self):
        return self.get_property_caldav_getctag()

    def get_property_webdav_getctag(self):
        return self.get_property_caldav_getctag()

    def get_property_caldav_getctag(self):
        return self.get_ctag()

    def get_ctag(self):
        return self.get_ctag_for_collection()

    def do_OPTIONS(self):
        """ Return a valid WebDAV OPTIONS response """
        methods = [
         'OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, COPY, MOVE',
         'PROPFIND, PROPPATCH, LOCK, UNLOCK, REPORT, ACL']
        self.request.simple_response(200, data=None, mimetype='text/plain', headers={'DAV': '1, 2, access-control, addressbook', 'Allow': (',').join(methods), 
           'Connection': 'close', 
           'MS-Author-Via': 'DAV'})
        return

    def _load_contents(self):
        accounts = self.context.run_command('account::get-all')
        for account in accounts:
            if account.carddav_uid is None:
                self.insert_child(account.object_id, account, alias=('{0}.vcf').format(account.object_id))
            else:
                self.insert_child(account.object_id, account, alias=account.carddav_uid)

        return True

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if name == '.ctag':
            return self.get_ctag_representation(self.get_ctag())
        else:
            if self.load_contents() and auto_load_enabled:
                if name in ('.json', '.ls'):
                    return self.get_collection_representation(name, self.get_children())
                if name == '.content.json':
                    return self.get_collection_representation(name, self.get_children(), rendered=True)
                result = self.get_child(name)
                if result is not None:
                    return self.get_entity_representation(name, result, location=('/dav/Contacts/{0}').format(name), is_webdav=is_webdav)
            self.no_such_path()
            return