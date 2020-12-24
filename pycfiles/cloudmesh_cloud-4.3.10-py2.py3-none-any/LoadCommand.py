# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/LoadCommand.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.default import Default
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.limits import Limits
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.ConfigDict import ConfigDict
import os

class LoadCommand(PluginCommand, CloudPluginCommand):
    topics = {'load': 'shell'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print('init command load')

    @command
    def do_load(self, args, arguments):
        """
        ::

            Usage:
                load MODULE [PYPI]

            ARGUMENTS:
               MODULE  The name of the module

            PREDEFINED MODULE NAMES:
               vbox    loads vbox command

            Examples:
                cm load cloudmesh_vagrant.cm_vbox.do_vbox
                    lists the plugins currently loaded

        """
        arg = dotdict(arguments)
        plugins = ConfigDict(filename='cloudmesh.yaml')
        if arg.MODULE == 'vbox':
            arg.MODULE = 'cloudmesh_vagrant.cm_vbox.do_vbox'
            arg.PYPI = 'cloudmesh_vagrant'
        if arg.PYPI is not None:
            try:
                import cloudmesh_vagrant
            except:
                os.system('pip install cloudmesh_vagrant')

        try:
            print('LOADING ->', arg.MODULE)
            self.load_instancemethod(arg.MODULE)
        except:
            Console.error(('Problem loading module {}').format(arg.MODULE), traceflag=True)

        return ''