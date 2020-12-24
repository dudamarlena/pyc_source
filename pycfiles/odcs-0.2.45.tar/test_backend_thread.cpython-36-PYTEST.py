# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/tests/test_backend_thread.py
# Compiled at: 2017-12-08 06:56:10
# Size of source mod 2**32: 2109 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from odcs.server.backend import BackendThread
from .utils import ModelsBaseTest
from mock import patch

class TestBackendThread(ModelsBaseTest):
    maxDiff = None

    def setUp(self):
        super(TestBackendThread, self).setUp()
        self.patch_do_work = patch('odcs.server.backend.BackendThread.do_work',
          autospec=True)
        self.do_work = self.patch_do_work.start()
        self.thread = BackendThread()

    def tearDown(self):
        super(TestBackendThread, self).tearDown()
        self.patch_do_work.stop()

    @patch('odcs.server.backend.db.session.rollback')
    def test_do_work_exception(self, rollback):

        def mocked_do_work(backend_thread):
            backend_thread.stop()
            raise ValueError('expected exception')

        self.do_work.side_effect = mocked_do_work
        self.thread._run()
        rollback.assert_called_once()