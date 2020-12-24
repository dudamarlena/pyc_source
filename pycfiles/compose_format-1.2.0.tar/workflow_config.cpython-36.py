# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/commands/subcommands/workflow_config.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 509 bytes
import os
from .base import BaseSubcommand

class WorkflowConfig(BaseSubcommand):
    remote_action = False
    setup_profile = False

    def cat(self):
        """
        Prints the loaded compose file to stdout
        """
        config_path = self.workflow.app_config_path
        if os.path.exists(config_path):
            with open(config_path, 'r') as (fh):
                print(fh.read())

    @classmethod
    def fill_subparser(cls, parser, subparser):
        subparser.add_argument('action')