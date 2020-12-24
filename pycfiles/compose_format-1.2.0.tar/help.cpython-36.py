# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/commands/subcommands/help.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 435 bytes
__doc__ = '\nWelcome to Docker Compose Workflows!\n\nThis is a utility around Docker Compose to make it easier to use\naround commonly used workflows within your development team.\n'
from .base import BaseSubcommand

class Help(BaseSubcommand):
    """Help"""

    @classmethod
    def fill_subparser(self, parser, subparser):
        pass

    def handle(self):
        self.print_subcommand_help(__doc__)