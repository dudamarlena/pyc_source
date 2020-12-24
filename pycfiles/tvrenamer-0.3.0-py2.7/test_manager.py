# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/tests/test_manager.py
# Compiled at: 2015-11-08 18:31:47
import mock
from tvrenamer import manager
from tvrenamer.processors import base as proc_base
from tvrenamer.tests import base

class ManagerTests(base.BaseTest):

    def setUp(self):
        super(ManagerTests, self).setUp()

    def test_run(self):
        with mock.patch.object(manager, '_start') as (mock_start):
            manager.run()
            self.assertTrue(mock_start.called)

    @mock.patch('tvrenamer.core.watcher.retrieve_files')
    @mock.patch.object(manager.episode, 'Episode')
    def test_start(self, mock_ep, mock_watcher):
        proc_mgr = mock.Mock(spec=proc_base.EnabledExtensionManager)
        mock_watcher.return_value = ['/tmp/videos/video1.mp4']
        manager._start(proc_mgr)
        self.assertTrue(proc_mgr.map_method.called)