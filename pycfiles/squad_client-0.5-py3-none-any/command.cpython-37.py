# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/squad_client/core/command.py
# Compiled at: 2020-02-21 13:41:57
# Size of source mod 2**32: 582 bytes


class SquadClientCommand:
    command = None
    help_text = None
    klasses = {}

    @staticmethod
    def add_commands(subparser):
        for klass in SquadClientCommand.__subclasses__():
            obj = klass()
            obj.register(subparser)
            SquadClientCommand.klasses[obj.command] = obj

    @staticmethod
    def process(args):
        return SquadClientCommand.klasses[args.command].run(args)

    def register(self, subparser):
        return subparser.add_parser((self.command), help=(self.help_text))

    def run(args):
        raise NotImplementedError