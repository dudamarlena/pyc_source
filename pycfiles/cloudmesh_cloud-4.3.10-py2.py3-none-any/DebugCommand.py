# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/DebugCommand.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default

class DebugCommand(PluginCommand, CloudPluginCommand):
    topics = {'debug': 'shell'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print('init command debug')
        try:
            value = Default.get_debug()
        except:
            Default.set_debug('off')

    @command
    def do_debug(self, args, arguments):
        """
        ::

            Usage:
                debug on
                debug off
                debug list

                switches on and off the debug messages

        """
        if arguments['on']:
            Default.set_debug('on')
            Console.ok('Switch debug on')
        elif arguments['off']:
            Default.set_debug('off')
            Console.ok('Switch debug off')
        elif arguments['list']:
            debug = Default.debug()
            Console.ok(('Debug is switched {}').format(debug))
        return ''