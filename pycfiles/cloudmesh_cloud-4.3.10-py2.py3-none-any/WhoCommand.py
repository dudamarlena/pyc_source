# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/WhoCommand.py
# Compiled at: 2017-04-23 10:30:41
from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.command import PluginCommand

class WhoCommand(PluginCommand):
    topics = {'Who ': 'system'}

    def __init__(self, context):
        self.context = context
        self.context.who_token = None
        if self.context.debug:
            Console.ok('init Who command')
        return

    @command
    def do_who(self, args, arguments):
        """
        ::

            Usage:
               who  hostname

        """
        try:
            logon = who.logon()
            if logon is False:
                Console.error('Could not logon')
                return
        except:
            Console.error('Could not logon')

        output_format = arguments['--format'] or 'table'
        if arguments['status']:
            pass
        ValueError('NOT yet implemented')
        return ''