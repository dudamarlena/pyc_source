# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pywebuml\tests\parsers\java\test_package_manager.py
# Compiled at: 2011-04-03 14:52:20
"""
Has some tests for `pywebuml.parsers.java.package_manager`
"""
from unittest2 import TestCase
from pywebuml.parsers.java.package_manager import JavaPackageManager

class TestJavaPackageManager(TestCase):

    def test_parse_content(self):
        """ Test parsing the content of a file.
        """
        content = [
         'package mypackage;',
         'import another.package.Bar;',
         'import other.*;',
         'public class Foo',
         '{',
         'public Bar bar;',
         'public Another another;}']
        package_manager = JavaPackageManager(content)
        self.assertEquals(package_manager.get_class_package(4), 'mypackage')
        self.assertEquals(package_manager.get_package_for_type('Bar'), 'another.package.Bar')
        self.assertEquals(package_manager.get_package_for_type('Another'), 'mypackage.Another')

    def test_parse_content_without_package(self):
        """ Test what happens when there is no package definition in the file.
        """
        content = [
         'import another.package.Bar;',
         'import other.*;',
         'public class Foo',
         '{',
         'public Bar bar;',
         'public Another another;}']
        package_manager = JavaPackageManager(content)
        self.assertEquals(package_manager.get_class_package(4), '')
        self.assertEquals(package_manager.get_package_for_type('Bar'), 'another.package.Bar')
        self.assertEquals(package_manager.get_package_for_type('Another'), 'Another')