# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/account/get_cabinets.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand

class GetCabinets(GetCommand):
    __domain__ = 'account'
    __operation__ = 'get-cabinets'
    mode = None

    def __init__(self):
        GetCommand.__init__(self)

    def parse_parameters(self, **params):
        GetCommand.parse_parameters(self, **params)

    def run(self):
        db = self._ctx.db_session()
        self.mode = 2
        if len(self.object_ids) == 0:
            self.object_ids.append(self._ctx.account_id)
        projects = self._ctx.run_command('account::get-projects', kind='opengroupware.coils.cabinet')
        folders = []
        for project in projects:
            folder = self._ctx.run_command('project::get-root-folder', project=project)
            if folder is not None:
                folders.append(folder)

        self.access_check = False
        self.set_return_value(folders)
        return