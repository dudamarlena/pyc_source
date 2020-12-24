# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/ResetCommand.py
# Compiled at: 2017-05-15 14:43:21
from __future__ import print_function
from cloudmesh_client.common.util import path_expand
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
import os
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand

class ResetCommand(PluginCommand, CloudPluginCommand):
    topics = {'reset': 'cloud'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print('init command reset')

    @command
    def do_reset(self, args, arguments):
        """
        ::

          Usage:
              reset

        Description:

            DANGER: This method erases the database.

        Examples:
            clean

        """
        filename = path_expand('~/.cloudmesh/cloudmesh.db')
        if os.path.exists(filename):
            os.remove(filename)
        Console.ok('Database reset')
        r = self.do_quit(None)
        Console.error('Quitting the shell does not yet work. please exit the shell now.')
        return ''