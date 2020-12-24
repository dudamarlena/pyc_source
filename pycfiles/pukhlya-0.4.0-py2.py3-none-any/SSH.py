# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: puke/SSH.py
# Compiled at: 2012-01-27 11:55:58
import paramiko, logging

class SSH(paramiko.SSHClient):

    def __init__(self):
        logger = paramiko.util.logging.getLogger('paramiko')
        logger.setLevel(logging.ERROR)
        super(SSH, self).__init__()

    def execute(self, cmd):
        chan = self.get_transport().open_session()
        chan.exec_command(cmd)
        return (
         chan.makefile('rb', -1).read(), chan.makefile_stderr('rb', -1).read(), chan.recv_exit_status())