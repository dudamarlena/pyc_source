# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/LauncherCommand.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from pprint import pprint
from cloudmesh_client.cloud.launcher import Launcher
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.default import Default
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand, CometPluginCommand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.hostlist import Parameter
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.Printer import Printer

class LauncherCommand(PluginCommand, CloudPluginCommand, CometPluginCommand):
    topics = {'launcher': 'todo'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print('init command launcher')

    @command
    def do_launcher(self, args, arguments):
        """
        ::

          Usage:
              launcher repo add NAME URL
              launcher repo delete NAME
              launcher repo list
              launcher repo
              launcher list [NAMES] [--cloud=CLOUD] [--format=FORMAT] [--source=db|dir]
              launcher add NAME SOURCE
              launcher delete [NAMES] [--cloud=CLOUD]
              launcher clear
              launcher run [NAME]
              launcher resume [NAME]
              launcher suspend [NAME]
              launcher refresh
              launcher log [NAME]
              launcher status [NAME]

          Arguments:

            KEY    the name of the launcher

          Options:

             --cloud=CLOUD    the name of the cloud
             --format=FORMAT  the output format [launcher: table]
             --all            lists all the launcher values

        Description:

        Launcher is a command line tool to test the portal launch
        functionalities through command line.

        The current launcher values can by listed with --all option:(
        if you have a launcher cloud specified. You can also add a
        cloud parameter to apply the command to a specific cloud)

               launcher list

            A launcher can be deleted with

                launcher delete KEY

        Examples:
            launcher list --all
            launcher list --cloud=general
            launcher delete <KEY>
        """
        print('AAA')
        arg = dotdict(arguments)
        if arg.NAMES is not None:
            arg.names = Parameter.expand(arg.NAMES)
        else:
            arg.names = None
        if arg.name == ['all']:
            arg.names = None
        arg.cloud = arguments['--cloud'] or Default.cloud
        arg.output = arguments['--format'] or 'table'
        arg.source = arguments['--source'] or 'db'
        print('BBB')
        pprint(arg)
        if arg.cloud is None:
            Console.error('Default arg.cloud not set')
            return
        else:
            result = ''
            if arguments['repo'] and arguments['list']:
                print('repo list')
                launchers = ConfigDict(filename='cm_launcher.yaml')['cloudmesh']['repo']
                print('repo add')
                d = {}
                for name in launchers:
                    location = launchers[name]['location']
                    d[name] = {'name': name, 'location': location}

                print(Printer.dict_table(d))
                return ''
            if arguments['repo'] and arguments['add']:
                launchers = ConfigDict(filename='cm_launcher.yaml')
                print('repo add')
                print(launchers)
                return ''
            if arguments['repo'] and arguments['delete']:
                print('repo delete')
                return ''
            if arguments['repo'] and not arguments['list']:
                print(arg.names)
                result = Launcher.list(name=arg.names, output=arg.output)
            elif arguments['add']:
                result = Launcher.add(name=arg.NAME, source=arg.SOURCE)
            elif arguments['delete']:
                for name in arg.names:
                    result = Launcher.delete(name=name, category=arg.cloud)

            elif arguments['run']:
                result = Launcher.run()
            elif arguments['resume']:
                result = Launcher.resume(name=arg.name)
            elif arguments['suspend']:
                result = Launcher.suspend(name=arg.name)
            elif arguments['details']:
                result = Launcher.details(name=arg.name)
            elif arguments['clear']:
                result = Launcher.clear()
            elif arguments['refresh']:
                result = Launcher.refresh(name=arg.name)
            print(result)
            return