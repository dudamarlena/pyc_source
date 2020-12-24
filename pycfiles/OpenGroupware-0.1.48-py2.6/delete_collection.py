# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/delete_collection.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import DeleteCommand

class DeleteCollection(DeleteCommand):
    __domain__ = 'collection'
    __operation__ = 'delete'

    def get_by_id(self, object_id, access_check):
        return self._ctx.run_command('collection::get', id=object_id, access_check=access_check)

    def run(self):
        DeleteCommand.run(self)