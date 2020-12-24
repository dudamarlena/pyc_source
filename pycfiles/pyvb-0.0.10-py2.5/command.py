# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyvb/command.py
# Compiled at: 2008-04-07 12:43:58
"""
command - pyvb module that holds a simple command abstraction
used to run VirtualBox commands.
"""
import popen2
from pyvb.exception import vbCommandError

class VBCommand:
    """An abstraction representing a command line command."""

    def __init__(self, command=''):
        """Constructor.  Initialize the command to run.
                @keyword command: The command to run.
                @type command: String
                @return: A new L{pyvb.command.VBCommand} instance.
                @rtype: L{pyvb.command.VBCommand}"""
        self.command = command

    def run(self):
        """Run the command and set the read, write, and error attributes.
                If there was and error, and exception is raised.
                @return: None
                @rtype: None"""
        (self.read, self.write, self.error) = popen2.popen3(self.command)
        error_message = self.error.read()
        if error_message:
            raise vbCommandError(error_message)