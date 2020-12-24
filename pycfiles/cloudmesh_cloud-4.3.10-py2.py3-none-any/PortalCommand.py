# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/PortalCommand.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.setup import os_execute

class PortalCommand(PluginCommand, CloudPluginCommand):
    topics = {'portal': 'cloud'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print('init command portal')

    def get_conf(self):
        config = ConfigDict('cloudmesh.yaml')
        data = dict(config['cloudmesh.portal'])
        print(data)
        return data

    @command
    def do_portal(self, args, arguments):
        """
        ::

            Usage:
                portal start
                portal stop

            Examples:
                portal start
                    starts the portal and opens the default web page

                portal stop
                    stops the portal

        """
        if arguments['start']:
            ValueError('Not yet implemented')
            data = self.get_conf()
            commands = ('\n                cd {location}; make run &\n                cd {location}; make view &\n                ').format(**data)
            print(data)
            os_execute(commands)
        if arguments['start']:
            ValueError('Not yet implemented')
            data = self.get_conf()
            commands = ('\n                cd {location}; make run\n                ').format(**data)
            print(data)
            os_execute(commands)
        elif arguments['stop']:
            ValueError('Not yet implemented')
        return ''