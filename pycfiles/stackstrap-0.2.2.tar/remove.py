# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/evelo/Documents/Repos/stackstrap/stackstrap/commands/template/remove.py
# Compiled at: 2014-01-13 23:26:55
from stackstrap.commands import Command, CommandError
from stackstrap.template import Template

class Remove(Command):
    """Remove a template"""
    name = 'remove'

    def setup_parser(self, parser):
        self.parser = parser
        self.parser.add_argument('name', metavar='NAME', help='The name of the template to remove')

    def main(self, args):
        template = Template(args.name)
        if not template.exists:
            raise CommandError('Invalid template name: %s' % args.name)
        self.log.info("Removing template '%s'" % template.name)
        template.delete()