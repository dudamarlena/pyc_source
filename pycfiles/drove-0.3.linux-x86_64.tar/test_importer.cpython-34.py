# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/tests/util/test_importer.py
# Compiled at: 2015-01-20 05:42:58
# Size of source mod 2**32: 737 bytes
import os, sys, unittest
from drove.util.importer import load

class TestImporter(unittest.TestCase):

    def test_importer_default(self):
        """Testing importer.load: from standard library"""
        cl = load('unittest.main', 'TestProgram')
        assert cl.__name__ == 'TestProgram'

    def test_importer_path(self):
        """Testing importer.load: from path"""
        path = os.path.dirname(__file__)
        cl = load('test_importer', 'TestImporter', path=[path])
        assert cl.__name__ == 'TestImporter'

    def test_importer_module(self):
        """Testing importer.load: module"""
        mod = load('sys')
        assert mod == sys