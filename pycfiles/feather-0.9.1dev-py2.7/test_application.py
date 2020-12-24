# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/feather/test/test_application.py
# Compiled at: 2011-06-15 17:38:25
import unittest
from feather import Application, Plugin

class ApplicationTest(unittest.TestCase):

    def setUp(self):
        self.commands = set(['one', 'two', 'three', 'APP_START', 'APP_STOP'])
        self.app = Application(self.commands)

    def test_create_application(self):
        self.assertEqual(self.app.needed_listeners, self.commands)
        self.assertEqual(self.app.needed_messengers, self.commands)
        self.assertFalse(self.app.valid)