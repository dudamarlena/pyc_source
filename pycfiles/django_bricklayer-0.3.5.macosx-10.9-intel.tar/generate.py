# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/bricklayer/management/commands/generate.py
# Compiled at: 2013-11-21 19:28:55
from django.core.management.base import BaseCommand, handle_default_options, OutputWrapper, OptionParser, CommandError
from django.core.management import get_commands, load_command_class
from bricklayer.management.commands import *
import sys, traceback

class Command(BaseCommand):
    help = 'Command dispatcher'
    args = '[command_name]'

    def run_from_argv(self, argv):
        """
        Command dispatcher.
        """
        self.stderr = OutputWrapper(sys.stderr, self.style.ERROR)
        command_name = argv.pop(2)
        command = self.__get_command_by_name(command_name)
        options, args = OptionParser(option_list=command.option_list).parse_args(argv[2:])
        handle_default_options(options)
        try:
            command.execute(*args, **options.__dict__)
        except Exception as e:
            if options.traceback:
                self.stderr.write(traceback.format_exc())
            else:
                self.stderr.write('%s: %s' % (e.__class__.__name__, e))
            sys.exit(1)

    def __get_command_by_name(self, command_name):
        if command_name == 'admin':
            command = GenerateAdminCommand()
        elif command_name == 'commandtest':
            command = TestCommand()
        elif command_name == 'command':
            command = GenerateCommandCommand()
        elif command_name == 'crud':
            command = GenerateCrudCommand()
        elif command_name == 'form':
            command = GenerateFormCommand()
        elif command_name == 'test':
            command = GenerateTestCommand()
        elif command_name == 'testpackage':
            command = GenerateTestPackageCommand()
        else:
            self.stderr.write('Unknown command: %s\n' % command_name)
            sys.exit(1)
        return command