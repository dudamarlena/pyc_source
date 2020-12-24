# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/vmalloc/sentinels/tests/test__readme_doctest.py
# Compiled at: 2016-08-30 03:19:06
from unittest import TestCase
import os, doctest

class ReadMeDocTest(TestCase):

    def test__readme_doctests(self):
        readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'README.rst'))
        self.assertTrue(os.path.exists(readme_path))
        result = doctest.testfile(readme_path, module_relative=False)
        self.assertEqual(result.failed, 0, '%s tests failed!' % result.failed)