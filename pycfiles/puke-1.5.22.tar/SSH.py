# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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