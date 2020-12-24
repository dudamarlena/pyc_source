# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/doc/ftpputfile.py
# Compiled at: 2012-10-12 07:02:39
from ftplib import FTP
from shutil import copyfileobj
from coils.core import *
from coils.core.logic import ActionCommand

class FTPPutFileAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'ftp-put-file'
    __aliases__ = ['ftpPutFile', 'ftpPutFileAction']

    def __init__(self):
        ActionCommand.__init__(self)

    @property
    def result_mimetype(self):
        return 'text/plain'

    def authentication_callback(self, server, share, workgroup, username, password):
        return (
         self._domain_string, self._username_string, self._password_string)

    def do_action(self):
        ftp = FTP(self._hostname)
        ftp.set_pasv(self._passive)
        if not self._username:
            ftp.login()
        else:
            ftp.login(self._username, self._password)
        if self._directory:
            ftp.cwd(self._directory)
        ftp.storbinary(('STOR {0}').format(self._filename), self._rfile)
        ftp.quit()

    def parse_action_parameters(self):
        self._hostname = self.process_label_substitutions(self.action_parameters.get('server'))
        self._filename = self.process_label_substitutions(self.action_parameters.get('filename'))
        self._passive = self.process_label_substitutions(self.action_parameters.get('passive', 'YES'))
        if not self._passive.upper() == 'NO':
            self._passive = True
        else:
            self._passive = False
        self._username = self.action_parameters.get('username', None)
        if self._username:
            self._username = self.process_label_substitutions(self._username)
            self._password = self.action_parameters.get('password', '$__EMAIL__;')
            self._password = self.process_label_substitutions(self._password)
        self._directory = self.action_parameters.get('directory', None)
        if self._directory:
            self._directory = self.process_label_substitutions(self._directory)
        return

    def do_epilogue(self):
        pass