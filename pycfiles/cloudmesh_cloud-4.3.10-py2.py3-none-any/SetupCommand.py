# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/SetupCommand.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand
from cloudmesh_client.default import Default
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.common.dotdict import dotdict
import os

class SetupCommand(PluginCommand, CloudPluginCommand):
    topics = {'setup': 'cloud'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print('init command setup')

    @command
    def do_setup(self, args, arguments):
        """
        ::

            Usage:
                setup

            Examples:
                cm setup

        """
        arg = dotdict(arguments)
        os.system('cm register profile')
        os.system('cm reset')
        os.system('cm key add --ssh')
        os.system('cm info')
        return ''