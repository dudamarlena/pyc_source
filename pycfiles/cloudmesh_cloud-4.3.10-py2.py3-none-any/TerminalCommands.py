# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/TerminalCommands.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
import os, sys
from builtins import input
from cloudmesh_client.shell.command import PluginCommand, ShellPluginCommand, CometPluginCommand
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
import time

class TerminalCommands(PluginCommand, ShellPluginCommand, CometPluginCommand):
    topics = {'clear': 'shell', 'echo': 'shell', 
       'puase': 'shell', 
       'banner': 'shell'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print('init command clear')
            print('init command banner')

    @command
    def do_clear(self, args, arguments):
        """
        Usage:
            clear

        Clears the screen."""
        sys.stdout.write(os.popen('clear').read())

    @command
    def do_sleep(self, args, arguments):
        """
        Usage:
            sleep SECONDS

        Clears the screen."""
        seconds = arguments['SECONDS']
        time.sleep(float(seconds))

    @command
    def do_echo(self, args, arguments):
        """
        ::

            Usage:
                echo  [-r COLOR] TEXT

            Arguments:
                TEXT   The text message to print
                COLOR  the color

            Options:
                -r COLOR  The color of the text. [default: BLACK]

            Prints a text in the given color
        """
        color = arguments['-r'] or 'black'
        color = color.upper()
        text = arguments['TEXT']
        if color is 'black':
            Console.msg(text)
        else:
            Console.cprint(color, '', text)
        return ''

    @command
    def do_banner(self, args, arguments):
        """
        ::

            Usage:
                banner [-c CHAR] [-n WIDTH] [-i INDENT] [-r COLOR] TEXT...

            Arguments:
                TEXT...   The text message from which to create the banner
                CHAR   The character for the frame.
                WIDTH  Width of the banner
                INDENT indentation of the banner
                COLOR  the color

            Options:
                -c CHAR   The character for the frame. [default: #]
                -n WIDTH  The width of the banner. [default: 70]
                -i INDENT  The width of the banner. [default: 0]
                -r COLOR  The color of the banner. [default: BLACK]

            Prints a banner form a one line text message.
        """
        Console.ok('banner')
        n = int(arguments['-n'])
        c = arguments['-c']
        i = int(arguments['-i'])
        color = arguments['-r'].upper()
        line = (' ').join(arguments['TEXT'])
        Console.cprint(color, '', i * ' ' + str((n - i) * c))
        Console.cprint(color, '', i * ' ' + c + ' ' + line)
        Console.cprint(color, '', i * ' ' + str((n - i) * c))
        return ''

    @command
    def do_pause(self, arg, arguments):
        """
        ::

            Usage:
                pause [MESSAGE]

            Displays the specified text then waits for the user to press RETURN.

            Arguments:
               MESSAGE  message to be displayed
        """
        if arguments['MESSAGE'] is None:
            arg = 'Press ENTER to continue'
        input(arg + '\n')
        return ''

    def set_verbose(self, on):
        pass

    def set_banner(self, banner):
        self.banner = banner

    @command
    def do_verbose(self, args, arguments):
        """
        Usage:
            verbose (True | False)
            verbose

        NOTE: NOT YET IMPLEMENTED.
        If it sets to True, a command will be printed before execution.
        In the interactive mode, you may want to set it to False.
        When you use scripts, we recommend to set it to True.

        The default is set to False

        If verbose is specified without parameter the flag is
        toggled.

        """
        Console.error('verbose NOT YET IMPLEMENTED')
        return ''