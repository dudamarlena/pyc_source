# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/fileinput_unit_test_no_file.py
# Compiled at: 2010-08-05 11:04:07
from fileinputwatcher import FileInputWatcher
from time import sleep
import unittest, os, Queue

class FileInputTestCase(unittest.TestCase):
    """test if the threaded callback is working when file created"""

    def test_file_add(self):
        self.queue = Queue.Queue(0)
        dir = '/home/eric/Desktop'
        file_input_watcher = FileInputWatcher(dir, self.queue)
        if os.path.isfile('/home/eric/Desktop/anyfile') is True:
            os.remove('/home/eric/Desktop/anyfile')
        file_input_watcher.monitor()
        sleep(1)
        try:
            result = self.queue.get(block='true', timeout=5)
        except Queue.Empty:
            result = None

        file_input_watcher.stop_monitoring()
        if os.path.isfile('/home/eric/Desktop/anyfile') is True:
            os.remove('/home/eric/Desktop/anyfile')
        self.assertEqual(result, None)
        return


if __name__ == '__main__':
    unittest.main()