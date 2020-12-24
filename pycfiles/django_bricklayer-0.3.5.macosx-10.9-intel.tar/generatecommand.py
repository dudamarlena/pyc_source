# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/bricklayer/testsuite/generatecommand.py
# Compiled at: 2013-11-21 19:28:55
from django.test import TestCase
from bricklayer.utils import *
import test_app, os, imp

class GenerateCommandTestCase(TestCase):

    def setUp(self):
        self.app_path = os.path.abspath(test_app.__path__[0])
        run_manage_py('generatecommand test_command test_app')

    def tearDown(self):
        try:
            os.remove(os.path.join(self.app_path, 'management', 'commands', '__init__.py'))
            os.remove(os.path.join(self.app_path, 'management', 'commands', 'test_command.py'))
            os.remove(os.path.join(self.app_path, 'management', '__init__.py'))
            os.rmdir(os.path.join(self.app_path, 'management', 'commands'))
            os.rmdir(os.path.join(self.app_path, 'management'))
        except:
            pass

    def test_commands(self):
        msg = ''
        self.assertTrue(exists_path(self.app_path, 'management'), msg)
        self.assertTrue(os.path.isdir(os.path.join(self.app_path, 'management')), msg)
        self.assertTrue(exists_path(self.app_path, 'management', 'commands'), msg)
        self.assertTrue(os.path.isdir(os.path.join(self.app_path, 'management', 'commands')), msg)
        self.assertTrue(exists_path(self.app_path, 'management', '__init__.py'), msg)
        self.assertTrue(exists_path(self.app_path, 'management', 'commands', '__init__.py'), msg)
        self.assertTrue(exists_path(self.app_path, 'management', 'commands', 'test_command.py'), msg)

    def test_shortcut_creation(self):
        command_module = imp.load_source('commands', os.path.join(self.app_path, 'management', 'commands', '__init__.py'))
        self.assertIn('TestCommandCommand', dir(command_module))