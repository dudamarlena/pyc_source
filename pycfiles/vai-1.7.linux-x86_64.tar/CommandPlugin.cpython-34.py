# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/sdk/CommandPlugin.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 923 bytes
from yapsy.IPlugin import IPlugin

class CommandPlugin(IPlugin):
    __doc__ = '\n    A base class to implement command plugins.\n\n    A command plugin is invoked when the : key is used. The first\n    word after the colon is the plugin keyword. When the keyword matches,\n    the method execute() is called\n    '

    def __init__(self):
        pass

    def name(self):
        """Returns the name of the plugin. To be reimplemented"""
        pass

    def keyword(self):
        """The keyword to activate the plugin."""
        pass

    def execute(self, command_line):
        """
        Method that handles the command.
        It receives the full command line as a string, meaning that it can do pretty much everything.
        If it fails, it's responsibility of the plugin to communicate the error condition.
        Return False if execution failed. True if successful.
        """
        return False