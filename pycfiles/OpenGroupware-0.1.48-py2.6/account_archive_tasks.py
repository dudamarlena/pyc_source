# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/gw/account_archive_tasks.py
# Compiled at: 2012-10-12 07:02:39
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand

class ArchiveAccountTasksAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'archive-account-tasks'
    __aliases__ = ['archiveAccountTasks', 'archiveAccountTasksAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def _get_object_id_from_input(self):
        doc = etree.parse(self.rfile)
        return int(doc.getroot().get('objectId'))

    def do_action(self):
        if self._ctx.is_admin:
            if self._user_id is None:
                self._user_id = self._get_object_id_from_input()
            account = self._ctx.run_command('contact::get', id=self._user_id, include_archived=True)
            if account is not None:
                result = self._ctx.run_command('task::batch-archive', owner_id=account.object_id)
            else:
                raise CoilsException(('Unable to retrieve object for objectId#{0}').format(self._user_id))
            self.wfile.write(unicode(result))
        else:
            raise CoilsException('Insufficient privilages to invoke archiveAccountTasksAction')
        return

    def parse_action_parameters(self):
        self._user_id = self.action_parameters.get('objectId', None)
        if self._user_id is not None:
            self._user_id = int(self.process_label_substitutions(self._user_id))
        return