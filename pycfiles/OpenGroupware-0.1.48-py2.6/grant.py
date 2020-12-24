# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/flow/grant.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import ActionCommand

class GrantAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'grant-access'
    __aliases__ = ['grantAction', 'grant']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        self._ctx.run_command('object::set-acl', object=self.process, context_id=self._context_id, action=self._action, permissions=self._permissions)

    def parse_action_parameters(self):
        self._context_id = int(self.action_parameters.get('contextId'))
        self._action = self.action_parameters.get('action', 'allowed')
        if 'permissions' in self.action_parameters:
            self._permissions = self.action_parameters.get('permissions').lower().strip()
        elif self.action_parameters.get('write', 'NO').upper() == 'YES':
            self._permissions = 'wvrlid'
        elif self.action_parameters.get('read', 'NO').upper() == 'YES':
            self._permissions = 'rvl'
        else:
            self._permissions = 'vl'

    def do_epilogue(self):
        pass