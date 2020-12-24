# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/cm_shell_status.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.shell.command import command, PluginCommand, ShellPluginCommand

class cm_shell_status(PluginCommand, ShellPluginCommand):
    topics = {'status': 'cloud'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print('init status default')

    @command
    def do_status(self, args, arguments):
        """
        ::

          Usage:
              status
              status db
              status CLOUDS...

          Arguments:

          Options:

        """
        if arguments['db']:
            print('status db')
        elif arguments['CLOUDS']:
            print('status CLOUDS...')
        else:
            print('status')