# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/ssh/putfile.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import ActionCommand
from command import SSHAction

class SSHPutFileAction(ActionCommand, SSHAction):
    __domain__ = 'action'
    __operation__ = 'ssh-put-file'
    __aliases__ = ['sshPutFileAction', 'sshPutFile']
    mode = None

    def __init__(self):
        ActionCommand.__init__(self)

    def parse_action_parameters(self):
        ActionCommand.parse_action_parameters(self)
        SSHAction.parse_action_parameters(self)
        self._filename = self.action_parameters.get('filePath', None)
        if not self._filename:
            raise CoilsException('No filename provided for sshPutFileAction action')
        self._filename = self.process_label_substitutions(self._filename)
        return

    def do_action(self):
        self.initialize_client()
        private_key = self.initialize_private_key(path=self.path_to_private_key(), password=self._secret)
        transport = self.initialize_transport(self._hostname, self._hostport)
        if self.authenticate(transport=transport, username=self._username, private_key=private_key):
            self.put_file(transport=transport, path=self._filename, rfile=self.rfile)
        else:
            raise CoilsException('Unable to complete SSH authentication')
        self.close_transport(transport=transport)