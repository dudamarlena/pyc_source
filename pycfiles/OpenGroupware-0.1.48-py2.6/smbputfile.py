# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/doc/smbputfile.py
# Compiled at: 2012-10-12 07:02:39
import os, smbc
from shutil import copyfileobj
from coils.core import *
from coils.core.logic import ActionCommand

class SMBPutFileAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'smb-put-file'
    __aliases__ = ['smbPutFile', 'smbPutFileAction']

    def __init__(self):
        ActionCommand.__init__(self)

    @property
    def result_mimetype(self):
        return 'text/plain'

    def authentication_callback(self, server, share, workgroup, username, password):
        return (
         self._domain_string, self._username_string, self._password_string)

    def do_action(self):
        cifs = smbc.Context(auth_fn=self.authentication_callback)
        handle = cifs.open(self._target_unc, os.O_CREAT | os.O_WRONLY | os.O_TRUNC)
        copyfileobj(self._rfile, handle)
        handle.close()

    def parse_action_parameters(self):
        self._domain_string = self.process_label_substitutions(self.action_parameters.get('domain'))
        self._password_string = self.process_label_substitutions(self.action_parameters.get('password'))
        self._username_string = self.process_label_substitutions(self.action_parameters.get('username'))
        self._target_unc = self.process_label_substitutions(self.action_parameters.get('target'))

    def do_epilogue(self):
        pass