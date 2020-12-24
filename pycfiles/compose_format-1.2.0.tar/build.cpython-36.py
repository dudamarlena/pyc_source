# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/commands/subcommands/build.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 212 bytes
from .base import BaseBuildSubcommand

class Build(BaseBuildSubcommand):
    """Build"""
    dirty_working_copy_okay = True

    def handle(self):
        self.build()