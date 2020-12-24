# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/command.py
# Compiled at: 2017-04-23 10:30:41
import inspect, textwrap, shlex
from docopt import docopt

class PluginCommand(object):
    pass


class CloudPluginCommand(object):
    pass


class ShellPluginCommand(object):
    pass


class HPCPluginCommand(object):
    pass


class CometPluginCommand(object):
    pass


def command(func):
    '''
    A decorator to create a function with docopt arguments.
    It also generates a help function

    @command
    def do_myfunc(self, args):
        """ docopts text """
        pass

    will create

    def do_myfunc(self, args, arguments):
        """ docopts text """
        ...

    def help_myfunc(self, args, arguments):
        ... prints the docopt text ...

    :param func: the function for the decorator
    '''
    classname = inspect.getouterframes(inspect.currentframe())[1][3]
    name = func.__name__
    help_name = name.replace('do_', 'help_')
    doc = textwrap.dedent(func.__doc__)

    def new(instance, args):
        try:
            argv = shlex.split(args)
            arguments = docopt(doc, help=True, argv=argv)
            func(instance, args, arguments)
        except SystemExit as e:
            if args not in ('-h', '--help'):
                print 'Could not execute the command.'
                print e
            print doc

    new.__doc__ = doc
    return new