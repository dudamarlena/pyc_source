# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/tests/test_utils.py
# Compiled at: 2018-02-20 08:15:54
# Size of source mod 2**32: 1958 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, unittest
from mock import patch
import time
from odcs.server.utils import execute_cmd

class TestUtilsExecuteCmd(unittest.TestCase):

    def setUp(self):
        super(TestUtilsExecuteCmd, self).setUp()

    def tearDown(self):
        super(TestUtilsExecuteCmd, self).tearDown()

    def test_execute_cmd_timeout_called(self):
        start_time = time.time()
        with self.assertRaisesRegexp(RuntimeError, 'Compose has taken more time.*'):
            execute_cmd(['/usr/bin/sleep', '5'], timeout=1)
        stop_time = time.time()
        self.assertTrue(stop_time - start_time < 2)

    @patch('odcs.server.utils._kill_process_group')
    def test_execute_cmd_timeout_not_called(self, killpg):
        execute_cmd(['/usr/bin/true'], timeout=1)
        time.sleep(2)
        killpg.assert_not_called()