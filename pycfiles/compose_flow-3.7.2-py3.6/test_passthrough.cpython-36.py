# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_passthrough.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 719 bytes
from compose_flow.commands.subcommands.passthrough_base import PassthroughBaseSubcommand
from tests import BaseTestCase, mock

class TestPassthroughSubcommand(PassthroughBaseSubcommand):

    def fill_subparser(self, cls, parser):
        pass


class BaseSubcommandTestCase(BaseTestCase):

    @mock.patch('compose_flow.commands.subcommands.passthrough_base.os')
    def test_execute(self, *mocks):
        workflow = mock.Mock()
        command = TestPassthroughSubcommand(workflow)
        proc = command.execute('docker ps')
        sh_mock = self.sh_mock
        sh_mock.docker.assert_called_with('ps', _env=(workflow.environment.data.copy()))