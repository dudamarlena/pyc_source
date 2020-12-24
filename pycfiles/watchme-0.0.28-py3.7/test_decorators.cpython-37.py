# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchme/tests/test_decorators.py
# Compiled at: 2020-04-10 14:08:50
# Size of source mod 2**32: 1182 bytes
from watchme import get_watcher
from watchme.command import create_watcher
import unittest, tempfile, shutil
print('####################################################### test_decorators')

class TestDecorators(unittest.TestCase):

    def setUp(self):
        self.base = tempfile.mkdtemp()
        self.repo = create_watcher('pancakes', base=(self.base))
        self.cli = get_watcher('pancakes', base=(self.base))

    def tearDown(self):
        shutil.rmtree(self.base)

    def test_psutils_monitor(self):
        """test creation function, and basic watcher config"""
        print('Testing psutilsc.decorators.TerminalRunner')
        from watchme.tasks.decorators import TerminalRunner
        runner = TerminalRunner('sleep 2')
        runner.run()
        timepoints = runner.wait('monitor_pid_task')
        self.assertTrue(len(timepoints) == 1)


if __name__ == '__main__':
    unittest.main()