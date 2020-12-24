# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/ptysh_module.py
# Compiled at: 2016-08-03 23:00:14
from ptysh_util import Status
PRINT_FORMAT_PADDING = 30

class PtyshModule(object):
    _node_name = ''
    _command_list = []

    def __init__(self):
        self._command_list = [
         [
          'exit', 'exit', self.cmd_exit, False, True],
         [
          'list', 'command list', self.cmd_list, False, True]]

    def get_node_name(self):
        return self._node_name

    def set_node_name(self, in_node_name):
        self._node_name = in_node_name

    def get_command_list(self):
        return self._command_list

    def set_command(self, in_cmd_name, in_cmd_desc, in_cmd_func, in_hidden_flag, in_working):
        self._command_list.append([in_cmd_name, in_cmd_desc, in_cmd_func, in_hidden_flag, in_working])

    def cmd_exit(self):
        Status().set_sub_node(False)

    def cmd_list(self):
        for cmd in self._command_list:
            if cmd[3] == True or cmd[4] == False:
                continue
            print '%s%s' % (cmd[0].ljust(PRINT_FORMAT_PADDING), cmd[1])