# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chaws/linaro/src/linaro/squad_client/squad_client/core/command.py
# Compiled at: 2020-03-06 06:36:18
# Size of source mod 2**32: 598 bytes


class SquadClientCommand:
    command = None
    help_text = None
    klasses = {}

    @staticmethod
    def add_commands(subparser):
        for klass in SquadClientCommand.__subclasses__():
            obj = klass()
            if obj.register(subparser) is None:
                SquadClientCommand.klasses[obj.command] = obj

    @staticmethod
    def process(args):
        return SquadClientCommand.klasses[args.command].run(args)

    def register(self, subparser):
        return subparser.add_parser((self.command), help=(self.help_text))

    def run(args):
        raise NotImplementedError