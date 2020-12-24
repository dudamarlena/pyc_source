# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/InfoCommand.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand
from cloudmesh_client.default import Default
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.common.dotdict import dotdict

class InfoCommand(PluginCommand, CloudPluginCommand):
    topics = {'info': 'cloud'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print('init command info')

    @command
    def do_info(self, args, arguments):
        """
        ::

            Usage:
                info [--cloud=CLOUD] [--format=FORMAT]

            Options:
               --format=FORMAT  the output format [default: table]
               --cloud=CLOUD    the cloud name

            Examples:
                cm info

        """
        arg = dotdict(arguments)
        arg.cloud = arguments['--cloud'] or Default.cloud
        arg.FORMAT = arguments['--format'] or 'table'
        d = {'cloud': arg.cloud, 
           'key': Default.key, 
           'user': Default.user, 
           'vm': Default.vm, 
           'group': Default.group, 
           'secgroup': Default.secgroup, 
           'counter': Default.get_counter(name='name'), 
           'image': Default.get_image(category=arg.cloud), 
           'flavor': Default.get_flavor(category=arg.cloud), 
           'refresh': str(Default.refresh), 
           'debug': str(Default.debug), 
           'interactive': str(Default.interactive), 
           'purge': str(Default.purge)}
        order = [
         'cloud', 'key', 'user', 'vm', 'group', 'secgroup',
         'counter', 'image', 'flavor', 'refresh', 'debug', 'interactive', 'purge']
        print(Printer.attribute(d, order=order, output=arg.FORMAT, sort_keys=False))
        if d['key'] in ('TBD', '') or d['user'] in ('TBD', ''):
            msg = 'Please replace the TBD values'
            msg = msg + '\nSee Also: \n\n' + '    cm register profile \n' + '    cm default user=YOURUSERNAME\n'
            Console.error(msg, traceflag=False)
        return ''