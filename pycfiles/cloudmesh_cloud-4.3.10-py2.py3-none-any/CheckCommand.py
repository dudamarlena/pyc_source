# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/CheckCommand.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default

class CheckCommand(PluginCommand, CloudPluginCommand):
    topics = {'check': 'notimplemented'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print('init command check')

    @command
    def do_check(self, args, arguments):
        """
        ::

            Usage:
                check --cloud=CLOUD
                check

                checks some elementary setting for cloudmesh

            Options:
               --format=FORMAT  the output format [default: table]
               --cloud=CLOUD    the cloud name

            Examples:
                cm check
                cm check --cloud=kilo

        """
        cloud = arguments['--cloud'] or Default.cloud
        if cloud is None:
            Console.error("Default cloud doesn't exist")
        print(locals())
        Console.TODO('This command is not implemented yet', traceflag=False)
        Console.ok(('{:} ok').format(cloud))
        return ''