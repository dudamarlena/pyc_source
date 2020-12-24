# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/ColorCommand.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command, PluginCommand, ShellPluginCommand, CometPluginCommand
from cloudmesh_client.common.ConfigDict import ConfigDict

class ColorCommand(PluginCommand, ShellPluginCommand, CometPluginCommand):
    topics = {'color': 'shell'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print('init command color')

    @command
    def do_color(self, args, arguments):
        """
        ::

            Usage:
                color FLAG

            Arguments:

                FLAG    color mode flag ON/OFF

            Description:

                Global switch for the console color mode.
                One can switch the color mode on/off with
                    cm color ON
                    cm color OFF

                By default, the color mode is ON

            Examples:
                color ON
                color OFF
        """
        color_mode = True
        flag = arguments['FLAG'].lower()
        if flag in ('on', 'true'):
            color_mode = True
            Console.set_theme(color=True)
        elif flag in ('off', 'false'):
            color_mode = False
            Console.set_theme(color=False)
        else:
            Console.error('Invalid Flag')
            return
        config = ConfigDict('cloudmesh.yaml')
        config['cloudmesh']['system']['console_color'] = color_mode
        config.save()
        Console.color = color_mode
        Console.ok(('Color {:}').format(str(color_mode)))
        return ''