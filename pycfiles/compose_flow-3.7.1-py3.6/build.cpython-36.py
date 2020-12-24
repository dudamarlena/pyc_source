# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/commands/subcommands/build.py
# Compiled at: 2020-01-28 12:24:29
# Size of source mod 2**32: 212 bytes
from .base import BaseBuildSubcommand

class Build(BaseBuildSubcommand):
    __doc__ = '\n    Subcommand for building Docker images\n    '
    dirty_working_copy_okay = True

    def handle(self):
        self.build()