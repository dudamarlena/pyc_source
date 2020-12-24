# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/growlf/django/django-boto/djaboto/management/base.py
# Compiled at: 2012-12-01 00:46:32
import optparse, djaboto
from django.core.management.base import BaseCommand

class CommandError(Exception):
    pass


class BaseCommand(BaseCommand):
    """
    Override version of Django's BaseCommand needed strictly for
    djaboto.
    """

    def version(self):
        return djaboto.get_version()

    def usage(self, command):
        usage = '%%prog %s [options] %s' % (command, self.args)
        if self.help:
            return '%s\n\n%s' % (usage, self.help)
        else:
            return usage

    def create_parser(self, prog_name, command):
        return optparse.OptionParser(prog=prog_name, usage=self.usage(command), version=self.version(), option_list=self.option_list)

    def print_help(self, prog_name, command):
        parser = self.create_parser(prog_name, command)
        parser.print_help()

    def run_from_argv(self, argv):
        parser = self.create_parser(argv[0], argv[1])
        options, args = parser.parse_args(argv[2:])
        self.handle(*args, **options.__dict__)