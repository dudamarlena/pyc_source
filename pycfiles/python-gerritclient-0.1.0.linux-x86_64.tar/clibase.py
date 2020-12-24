# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/machin/.virtualenvs/twine/lib/python2.7/site-packages/gerritclient/tests/unit/cli/clibase.py
# Compiled at: 2018-01-03 08:48:28
import shlex, mock
from oslotest import base as oslo_base
from gerritclient import client
from gerritclient import main as main_mod

class BaseCLITest(oslo_base.BaseTestCase):
    """Base class for testing CLI."""

    def setUp(self):
        super(BaseCLITest, self).setUp()
        self._get_client_patcher = mock.patch.object(client, 'get_client')
        self.m_get_client = self._get_client_patcher.start()
        self.m_client = mock.MagicMock()
        self.m_get_client.return_value = self.m_client
        self.addCleanup(self._get_client_patcher.stop)

    @staticmethod
    def exec_command(command=''):
        """Executes gerrit with the specified arguments."""
        argv = shlex.split(command)
        if '--debug' not in argv:
            argv = argv + ['--debug']
        return main_mod.main(argv=argv)