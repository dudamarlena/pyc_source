# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/gw/get_user_account.py
# Compiled at: 2012-10-12 07:02:39
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand
from coils.core.xml import Render as XML_Render

class GetUserAccountAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'get-user-account'
    __aliases__ = ['getUserAccountAction', 'getUserAccount']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        self.log.debug(('Attempting to retrieve Omphalos XML representation of login "{0}"').format(self._login))
        entity = self._ctx.run_command('account::get', login=self._login)
        if entity is not None:
            results = XML_Render.render(entity, self._ctx)
            self.wfile.write(results)
        else:
            self.log.error(('Unable to retrieve Omphalos XML representation of login "{0}"').format(self._login))
        return

    @property
    def result_mimetype(self):
        return 'application/xml'

    def parse_action_parameters(self):
        self._login = self.action_parameters.get('login', None)
        if self._login is not None:
            self._login = self.process_label_substitutions(self._login)
        else:
            self._login = self._ctx.login
        return

    def do_epilogue(self):
        pass