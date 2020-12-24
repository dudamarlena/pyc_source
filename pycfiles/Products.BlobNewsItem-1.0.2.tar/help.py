# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteScript-1.7.5-py2.6.egg/paste/script/help.py
# Compiled at: 2012-02-27 07:41:53
from command import Command, get_commands
from command import parser as base_parser

class HelpCommand(Command):
    summary = 'Display help'
    usage = '[COMMAND]'
    max_args = 1
    parser = Command.standard_parser()

    def command(self):
        if not self.args:
            self.generic_help()
            return
        name = self.args[0]
        commands = get_commands()
        if name not in commands:
            print 'No such command: %s' % name
            self.generic_help()
            return
        command = commands[name].load()
        runner = command(name)
        runner.run(['-h'])

    def generic_help(self):
        base_parser.print_help()
        print
        commands_grouped = {}
        commands = get_commands()
        longest = max([ len(n) for n in commands.keys() ])
        for (name, command) in commands.items():
            try:
                command = command.load()
            except Exception, e:
                print 'Cannot load command %s: %s' % (name, e)
                continue

            if getattr(command, 'hidden', False):
                continue
            commands_grouped.setdefault(command.group_name, []).append((name, command))

        commands_grouped = commands_grouped.items()
        commands_grouped.sort()
        print 'Commands:'
        for (group, commands) in commands_grouped:
            if group:
                print group + ':'
            commands.sort()
            for (name, command) in commands:
                print '  %s  %s' % (self.pad(name, length=longest),
                 command.summary)

            print