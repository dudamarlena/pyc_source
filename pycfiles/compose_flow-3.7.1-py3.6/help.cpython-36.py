# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/commands/subcommands/help.py
# Compiled at: 2020-01-28 12:24:29
# Size of source mod 2**32: 435 bytes
"""
Welcome to Docker Compose Workflows!

This is a utility around Docker Compose to make it easier to use
around commonly used workflows within your development team.
"""
from .base import BaseSubcommand

class Help(BaseSubcommand):
    __doc__ = '\n    Subcommand for managing profiles\n    '

    @classmethod
    def fill_subparser(self, parser, subparser):
        pass

    def handle(self):
        self.print_subcommand_help(__doc__)