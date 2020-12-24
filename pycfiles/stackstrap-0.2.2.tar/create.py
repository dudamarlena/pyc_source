# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/evelo/Documents/Repos/stackstrap/stackstrap/commands/template/create.py
# Compiled at: 2014-01-22 09:22:48
import os
from stackstrap.config import settings
from stackstrap.commands import Command
from stackstrap.template import Template, MASTER_TEMPLATE_URL

class Create(Command):
    """Create a new template"""
    name = 'create'

    def setup_parser(self, parser):
        self.parser = parser
        template_url = settings.get('project_template_url', MASTER_TEMPLATE_URL)
        self.parser.add_argument('path', metavar='PATH', type=str, help='The path to create the new template at')
        self.parser.add_argument('-t', '--template', metavar='GIT_URL', type=str, help='The GIT URL of the template to use. Defaults to %s' % template_url, default=template_url)
        self.parser.add_argument('-r', '--ref', metavar='GIT_REF', type=str, help='The GIT reference to use when archiving the template. Defaults to master.', default='master')

    def main(self, args):
        from stackstrap.cli import StackStrapCLI
        cli = StackStrapCLI()
        template = Template('master-template')
        if not template.exists:
            self.log.info("You are creating a new template for the first time we will now setup a template named 'master-template' that is used to create new templates.")
            cli.main(['template', 'add', '-r', args.ref, 'master-template', args.template])
        cli.main(['create', args.path, 'master-template'])