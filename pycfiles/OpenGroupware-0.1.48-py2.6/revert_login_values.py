# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/gw/revert_login_values.py
# Compiled at: 2012-10-12 07:02:39
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand
from coils.core.xml import Render as XML_Render

class RevertArchivedLoginValues(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'revert-archived-login-values'
    __aliases__ = ['revertArchivedLoginValues', 'revertArchivedLoginValuesAction']

    def __init__(self):
        ActionCommand.__init__(self)

    @property
    def mimetype(self):
        return 'text/plain'

    def do_action(self):
        if self._ctx.is_admin:
            query = self._ctx.db_session().query(Contact).filter(Contact.status == 'archived')
            for contact in query.all():
                login = ('OGo{0}').format(contact.object_id)
                if contact.login != login:
                    self._ctx.run_command('contact::set', object=contact, values={'login': login})
                    self.wfile.write(('Modified login of contactId#{0}').format(contact.object_id))

        else:
            raise CoilsException('Insufficient privilages to invoke removeAccountStatusAction')

    def parse_action_parameters(self):
        pass