# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Tests/LoadTemplate.py
# Compiled at: 2019-09-22 10:12:27
import os, unittest, Cheetah.ImportHooks
from Cheetah.LoadTemplate import loadTemplateClass
from Cheetah.Tests.ImportHooks import ImportHooksTemplatesDir, _cleanup
from Cheetah.Tests.ImportHooks import setUpModule, tearDownModule

class LoadTemplateTest(unittest.TestCase):

    def setUp(self):
        _cleanup()

    def tearDown(self):
        _cleanup()

    def test_loadTemplate(self):
        templates = os.listdir(ImportHooksTemplatesDir)
        self.assertNotIn('index.py', templates)
        self.assertNotIn('layout.py', templates)
        self.assertRaises(ImportError, loadTemplateClass, os.path.join(ImportHooksTemplatesDir, 'index.tmpl'))
        templates = os.listdir(ImportHooksTemplatesDir)
        self.assertIn('index.py', templates)
        self.assertNotIn('layout.py', templates)
        loadTemplateClass(os.path.join(ImportHooksTemplatesDir, 'layout.tmpl'))
        templates = os.listdir(ImportHooksTemplatesDir)
        self.assertIn('index.py', templates)
        self.assertIn('layout.py', templates)
        loadTemplateClass(os.path.join(ImportHooksTemplatesDir, 'index.tmpl'))
        self.assertRaises(ImportError, loadTemplateClass, 'doesnotexist')

    def test_ImportHooks(self):
        templates = os.listdir(ImportHooksTemplatesDir)
        self.assertNotIn('index.py', templates)
        self.assertNotIn('layout.py', templates)
        Cheetah.ImportHooks.install()
        loadTemplateClass(os.path.join(ImportHooksTemplatesDir, 'index.tmpl'))
        templates = os.listdir(ImportHooksTemplatesDir)
        self.assertIn('index.py', templates)
        self.assertIn('layout.py', templates)
        Cheetah.ImportHooks.uninstall()