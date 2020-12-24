# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymk/tests/extra/touch.py
# Compiled at: 2013-09-04 13:55:56
from time import sleep, time
import os
from pymk.tests.base import PymkTestCase
from pymk.extra import touch

class TouchTest(PymkTestCase):
    test_file = 'testme.file'

    def test_new_file(self):
        actual_time = int(time())
        touch(self.test_file)
        file_time = int(os.path.getmtime(self.test_file))
        self.assertTrue(os.path.exists(self.test_file))
        self.assertEqual(actual_time, file_time)

    def test_change_time(self):
        touch(self.test_file)
        first_file_time = os.path.getmtime(self.test_file)
        sleep(0.01)
        touch(self.test_file)
        second_file_time = os.path.getmtime(self.test_file)
        self.assertNotEqual(first_file_time, second_file_time)