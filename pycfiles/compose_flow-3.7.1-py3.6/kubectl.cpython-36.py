# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/commands/subcommands/kubectl.py
# Compiled at: 2020-01-28 12:24:29
# Size of source mod 2**32: 480 bytes
"""
Helm subcommand
"""
from compose_flow.kube.mixins import KubeMixIn
from .passthrough_base import PassthroughBaseSubcommand

class Kubectl(PassthroughBaseSubcommand, KubeMixIn):
    __doc__ = '\n    Subcommand for running rancher CLI commands\n    '
    command_name = 'kubectl'
    setup_environment = True
    setup_profile = False

    def handle(self, extra_args=None):
        self.switch_kube_context()
        return super().handle(log_output=False)