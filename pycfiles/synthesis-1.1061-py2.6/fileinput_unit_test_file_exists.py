# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/fileinput_unit_test_file_exists.py
# Compiled at: 2010-08-05 11:04:07
from fileinputwatcher import FileInputWatcher
from time import sleep
import unittest, os, Queue, testCase_settings

class FileInputTestCase(unittest.TestCase):
    """test if the threaded callback is working when file created"""

    def test_file_add(self):
        self.queue = Queue.Queue(0)
        dir = testCase_settings.INPUTFILES_PATH
        testFile = testCase_settings.TEST_FILE
        file_input_watcher = FileInputWatcher(dir, self.queue)
        if os.path.isfile(os.path.join(dir, testFile)) is True:
            os.remove(os.path.join(dir, testFile))
        file_input_watcher.monitor()
        sleep(1)
        f = open(os.path.join(dir, testFile), 'w')
        f.close()
        result = self.queue.get(block='true')
        if result is not None:
            file_input_watcher.stop_monitoring()
        if os.path.isfile(os.path.join(dir, testFile)) is True:
            os.remove(os.path.join(dir, testFile))
        self.assertEqual(result, os.path.join(dir, testFile))
        return


if __name__ == '__main__':
    unittest.main()