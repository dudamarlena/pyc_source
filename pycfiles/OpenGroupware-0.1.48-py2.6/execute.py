# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/ssh/execute.py
# Compiled at: 2012-10-12 07:02:39
import errno
from coils.core import *
from coils.core.logic import ActionCommand
from command import SSHAction

class SSHExecAction(ActionCommand, SSHAction):
    __domain__ = 'action'
    __operation__ = 'ssh-exec'
    __aliases__ = ['sshExecuteCommandAction', 'sshExecAction', 'sshExec', 'sshExecuteCommand']
    mode = None

    def __init__(self):
        ActionCommand.__init__(self)

    @property
    def result_mimetype(self):
        return self._mimetype

    def parse_action_parameters(self):
        ActionCommand.parse_action_parameters(self)
        SSHAction.parse_action_parameters(self)
        self._command = self.action_parameters.get('command', None)
        self._filename = self.action_parameters.get('filePath', None)
        self._mimetype = self.action_parameters.get('mimeType', 'application/octet-stream')
        if not self._command:
            raise CoilsException('No command string for executeSSHCommand action')
        self._command = self.process_label_substitutions(self._command)
        if self._filename:
            self._filename = self.process_label_substitutions(self._filename)
        return

    def do_action(self):
        self.initialize_client()
        private_key = self.initialize_private_key(path=self.path_to_private_key(), password=self._secret)
        transport = self.initialize_transport(self._hostname, self._hostport)
        if self.authenticate(transport=transport, username=self._username, private_key=private_key):
            self.run_command(transport=transport, command=self._command, wfile=self.wfile)
            if self._filename:
                try:
                    self.get_file(transport=transport, path=self._filename, wfile=self.wfile)
                except IOError, e:
                    if e.errno == errno.ENOENT:
                        raise CoilsException(('Path "{0}" on host "{1}" not found; could not retrieve file.').format(self._filename, self._hostname))
                    else:
                        raise e

        else:
            raise CoilsException('Unable to complete SSH authentication')
        self.close_transport(transport=transport)