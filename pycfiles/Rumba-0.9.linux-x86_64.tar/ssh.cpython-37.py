# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/rumba/executors/ssh.py
# Compiled at: 2018-07-25 06:08:30
# Size of source mod 2**32: 2076 bytes
from rumba.model import Executor
from rumba.ssh_support import execute_command, execute_commands, copy_file_to_testbed, copy_file_from_testbed

class SSHExecutor(Executor):

    def __init__(self, testbed):
        self.testbed = testbed

    def execute_command(self, node, command, as_root=False, time_out=3):
        return self.execute_commands(node, [command], as_root, time_out)

    def execute_commands(self, node, commands, as_root=False, time_out=3):
        if as_root:
            if node.ssh_config.username != 'root':
                commands = list(map(lambda c: 'sudo %s' % (c,), commands))
        return execute_commands(self.testbed, node.ssh_config, commands, time_out)

    def fetch_file(self, node, path, destination, sudo=False):
        copy_file_from_testbed(self.testbed, node.ssh_config, path, destination, sudo)

    def copy_file(self, node, path, destination):
        copy_file_to_testbed(self.testbed, node.ssh_config, path, destination)