# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/RefreshCommand.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default

class RefreshCommand(PluginCommand, CloudPluginCommand):
    topics = {'refresh': 'shell'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print('init command refresh')

    @command
    def do_refresh(self, args, arguments):
        """
        ::

            Usage:
                refresh on
                refresh off
                refresh [list]

                switches on and off the refresh for clouds

        """
        if arguments['on']:
            Default.set_refresh(True)
            Console.ok('Switch refresh on')
        elif arguments['off']:
            Default.set_refresh(False)
            Console.ok('Switch refresh off')
        else:
            refresh = Default.refresh
            if refresh:
                msg = 'on'
            else:
                msg = 'off'
            Console.ok(('Automatic cloud refresh is switched {}').format(msg))
        return ''