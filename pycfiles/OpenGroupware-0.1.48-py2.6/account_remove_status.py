# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/gw/account_remove_status.py
# Compiled at: 2012-10-12 07:02:39
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand
from coils.core.xml import Render as XML_Render

class RemoveAccountStatusAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'remove-account-status'
    __aliases__ = ['removeAccountStatus', 'removeAccountStatusAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def _get_object_id_from_input(self):
        try:
            doc = etree.parse(self.rfile)
        except Exception, e:
            return

        return int(doc.getroot().get('objectId'))
        return

    def do_action(self):
        if self._ctx.is_admin:
            if self._login is None:
                object_id = self._get_object_id_from_input()
                if object_id is not None:
                    account = self._ctx.run_command('account::get', id=object_id)
                else:
                    account = None
            else:
                account = self._ctx.run_command('account::get', login=self._login)
            if account is not None:
                if account.is_account == 1:
                    account.is_account = 0
                    account.version += 1
                    self.log.info(('account id#{0} {1} has been removed').format(account.object_id, account.login))
                    account.login = ('OGo{0}').format(account.object_id)
                    if self._archive == 'YES':
                        account.status = 'archived'
                        self.log.info(('contact id#{0} has been archived').format(account.object_id))
                    self.wfile.write('OK')
                else:
                    self.wfile.write('NOP')
            else:
                self.log.debug(('Unable to retrieve account with login "{0}"').format(self._login))
                self.wfile.write('FAIL')
        else:
            raise CoilsException('Insufficient privilages to invoke removeAccountStatusAction')
        return

    def parse_action_parameters(self):
        self._login = self.action_parameters.get('login', None)
        self._archive = self.action_parameters.get('archive', 'NO')
        if self._login is not None:
            self._login = self.process_label_substitutions(self._login)
        return