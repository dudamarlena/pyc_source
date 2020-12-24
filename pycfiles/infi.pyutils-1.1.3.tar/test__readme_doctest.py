# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Infinidat/infi.pyutils/tests/test__readme_doctest.py
# Compiled at: 2016-09-14 06:55:36
from .test_utils import TestCase
import os, doctest

class ReadMeDocTest(TestCase):

    def test__readme_doctests(self):
        readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'README.rst'))
        self.assertTrue(os.path.exists(readme_path))
        result = doctest.testfile(readme_path, module_relative=False)
        self.assertEquals(result.failed, 0, '%s tests failed!' % result.failed)