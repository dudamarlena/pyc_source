# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/blob/delete_version.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.foundation import *
from coils.core.logic import DeleteCommand
from command import BLOBCommand

class DeleteDocumentVersion(DeleteCommand, BLOBCommand):
    __domain__ = 'document'
    __operation__ = 'delete-version'

    def __init__(self):
        DeleteCommand.__init__(self)

    def parse_parameters(self, **params):
        if 'document' in params:
            self._document = params['document']
        elif 'id' in params:
            self._document = self._ctx.run_command('document::get', id=int(params['id']))
        else:
            raise CoilsException('')
        self._version = int(params.get('version', 1))

    def run(self):
        self.obj = self._ctx.run_command('document::get-version', document=self._document, version=self._version)
        manager = self.get_manager(self._document)
        if self.obj is not None:
            self.object_id = self.obj.object_id
            print ('going to delete object id #{0}').format(self.object_id)
            DeleteCommand.run(self)
            self.delete_version(manager, self._document, version=self._version)
            self._ctx.db_session().flush()
            self._ctx.db_session().refresh(self._document)
        return