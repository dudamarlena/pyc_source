# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymk/tests/error.py
# Compiled at: 2013-10-03 07:18:17
import unittest
from pymk import error

class ErrorsTests(unittest.TestCase):

    def test_CouldNotCreateFile(self):
        er = error.CouldNotCreateFile('filename')
        self.assertEqual(str, type(str(er)))

    def test_TaskAlreadyExists(self):
        er = error.TaskAlreadyExists('task name')
        self.assertEqual(str, type(str(er)))

    def test_CommandError(self):
        er = error.CommandError(1, 'task name')
        self.assertEqual(str, type(str(er)))

    def test_BadTaskName(self):
        er = error.BadTaskPath('task name')
        self.assertEqual(str, type(str(er)))

    def test_WrongArgumentValue(self):
        er = error.WrongArgumentValue('description')
        self.assertEqual(str, type(str(er)))

    def test_TaskMustHaveOutputFile(self):
        er = error.TaskMustHaveOutputFile('name')
        self.assertEqual(str, type(str(er)))

    def test_NoDependencysInAClass(self):
        er = error.NoDependencysInAClass(error.NoDependencysInAClass)
        self.assertEqual(str, type(str(er)))

    def test_NotADependencyError(self):
        er = error.NotADependencyError(error.NoDependencysInAClass, error.NoDependencysInAClass)
        self.assertEqual(str, type(str(er)))

    def test_RecipeAlreadyExists(self):
        er = error.RecipeAlreadyExists('name')
        self.assertEqual(str, type(str(er)))

    def test_WrongPymkVersion(self):
        er = error.WrongPymkVersion('pymk_version', 'mkfile_version')
        self.assertEqual(str, type(str(er)))