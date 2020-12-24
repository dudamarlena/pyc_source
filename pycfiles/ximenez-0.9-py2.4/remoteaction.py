# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.11.1-i386/egg/ximenez/actions/ssh/remoteaction.py
# Compiled at: 2007-12-01 11:00:28
"""Define ``SSHRemote``, a plug-in which can execute a command
on a remote host via SSH.

$Id: remoteaction.py 42 2007-12-01 16:00:28Z damien.baty $
"""
import os, logging
from ximenez.actions.action import Action
from ximenez.shared import ConnectionException

def getInstance():
    """Return an instance of ``SSHRemote``."""
    return SSHRemote()


class SSHRemote(Action):
    """Connect to remote hosts via SSH, execute a command and return
    its output.
    """
    __module__ = __name__
    _input_info = ({'name': 'command', 'prompt': 'Command: ', 'required': True},)

    def getInput(self, cl_input=None):
        """Get input from the user if what was provided in the command
        line (available in ``cl_input``) was not sufficient.

        If a value is given in the command line (``cl_input``), we
        suppose it is the command to execute.
        """
        if cl_input:
            self._input['command'] = cl_input
        else:
            Action.getInput(self, cl_input)

    def execute(self, sequence):
        """Connect to each host of ``sequence`` and execute a
        command.
        """
        command = self._input['command']
        for host in sequence:
            try:
                output = host.execute(command)
                logging.info('Executing "%s" on "%s":%s%s', command, host, os.linesep, output)
            except ConnectionException:
                logging.error('Could not connect to "%s".' % host)