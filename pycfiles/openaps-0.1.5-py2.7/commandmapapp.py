# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openaps/cli/commandmapapp.py
# Compiled at: 2015-12-15 13:09:24
from subcommand import Subcommand

class CommandMapApp(object):
    Subcommand = Subcommand
    commands = {}
    metavar = None

    def __init__(self, parent):
        self.parent = parent
        self.commands = {}

    def get_help(self):
        return 'Operation'

    def get_dest(self):
        return 'command'

    def get_description(self):
        return getattr(self, '__doc__', None)

    def get_title(self):
        return getattr(self, 'title', '## ' + getattr(self, 'title', self.__class__.__name__))

    def get_commands(self):
        return []

    def get_metavar(self):
        return self.metavar

    def configure_commands(self, parser):
        subparsers = parser.add_subparsers(title=self.get_title(), description=self.get_description(), help=self.get_help(), metavar=self.get_metavar(), dest=self.get_dest())
        self.subparsers = subparsers
        for ctx in self.get_commands():
            self.makeSubcommand(ctx)

        return self.commands

    def selected(self, args):
        selected = getattr(args, self.get_dest())
        return self.commands[selected]

    def get(self, name):
        return self.commands[name]

    def makeSubcommand(self, ctx):
        app = self.Subcommand(ctx, parent=self.parent)
        parser = app.configure_subparser(self.subparsers)
        app.configure_parser(parser)
        self.commands[app.name] = app