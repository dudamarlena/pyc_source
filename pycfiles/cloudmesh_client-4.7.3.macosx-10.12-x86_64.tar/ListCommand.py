# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/ListCommand.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.cloud.list import List
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default
from cloudmesh_client.cloud.image import Image
from cloudmesh_client.cloud.flavor import Flavor
from cloudmesh_client.cloud.vm import Vm
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand

class ListCommand(PluginCommand, CloudPluginCommand):
    topics = {'list': 'cloud'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print('init command list')

    @command
    def do_list(self, args, arguments):
        """
        ::

            Usage:
                list [--cloud=CLOUD] [--format=FORMAT] [--user=USER] [--tenant=TENANT] default
                list [--cloud=CLOUD] [--format=FORMAT] [--user=USER] [--tenant=TENANT] vm
                list [--cloud=CLOUD] [--format=FORMAT] [--user=USER] [--tenant=TENANT] flavor
                list [--cloud=CLOUD] [--format=FORMAT] [--user=USER] [--tenant=TENANT] image

            List the items stored in the database

            Options:
                --cloud=CLOUD    the name of the cloud
                --format=FORMAT  the output format
                --tenant=TENANT     Name of the tenant, e.g. fg82.

            Description:
                List command prints the values stored in the database
                for [default/vm/flavor/image].
                Result can be filtered based on the cloud, user & tenant arguments.
                If these arguments are not specified, it reads the default

            Examples:
                $ list --cloud india default
                $ list --cloud india --format table flavor
                $ list --cloud india --user albert --tenant fg82 flavor
        """

        def get_kind():
            for k in ['vm', 'image', 'flavor', 'default']:
                if arguments[k]:
                    return k.upper()

            return 'help'

        output_format = arguments['--format']
        cloud = arguments['--cloud'] or Default.cloud
        user = arguments['--user']
        tenant = arguments['--tenant']
        if output_format is None:
            output_format = Default.get(name='format') or 'table'
        if cloud is None:
            cloud = Default.get(name='cloud') or ConfigDict(filename='cloudmesh.yaml')['cloudmesh']['active'][0]
        if user is None:
            user = Default.get(name='user')
        if tenant is None:
            tenant = Default.get(name='tenant')
        kind = get_kind()
        header = None
        order = None
        if kind == 'help':
            Console.ok('Print help!')
            return ''
        else:
            result = None
            if kind == 'FLAVOR':
                result = Flavor.list(cloud, format=output_format)
            elif kind == 'DEFAULT':
                result = Default.list(order=order, output=output_format)
            elif kind == 'IMAGE':
                result = Image.list(cloud, format=output_format)
            elif kind == 'VM':
                result = Vm.list(cloud=cloud, output_format=output_format)
            if result:
                print(result)
            else:
                Console.error(('No {}s found in the database.').format(kind.lower()))
            return ''