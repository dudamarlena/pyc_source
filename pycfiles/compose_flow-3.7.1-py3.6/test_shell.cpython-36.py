# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_shell.py
# Compiled at: 2020-01-28 12:24:29
# Size of source mod 2**32: 468 bytes
from unittest import TestCase, mock
from compose_flow import shell
from tests import BaseTestCase

class ShellTestCase(BaseTestCase):

    @mock.patch('compose_flow.shell.OS_ENV_INCLUDES', new_callable=dict)
    def test_execute(self, *mocks):
        """
        Ensure the shell's execution is done with the passed in environment
        """
        env = {}
        shell.execute('docker ps', env)
        self.sh_mock.docker.assert_called_with('ps', _env=env)