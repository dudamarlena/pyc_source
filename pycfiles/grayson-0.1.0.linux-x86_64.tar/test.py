# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/scox/dev/grayson/venv/lib/python2.7/site-packages/grayson/test.py
# Compiled at: 2012-03-02 14:59:52
"""

Grayson unit tests.

"""
import unittest, shutil, os
from grayson.packager import GraysonPackager
from grayson.compiler import GraysonCompiler

class TestGrayson(unittest.TestCase):

    def setUp(self):
        self.log_level = None
        self.output_dir = 'test-output'
        self.model_patterns = os.path.join('model', '*.graphml')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.output_file = os.path.join(self.output_dir, 'test-archive.zip')
        self.unpack_output_dir = os.path.join(self.output_dir, 'unpack')
        return

    def test_package_archive(self):
        GraysonPackager.package(patterns=[self.model_patterns], output_file=self.output_file, logLevel=self.log_level)

    def test_verify_archive(self):
        GraysonPackager.verify(input_file=self.output_file, logLevel=self.log_level)

    def test_compile(self):
        GraysonPackager.unpack(input_file=self.output_file, output_dir=self.unpack_output_dir, logLevel=self.log_level)
        self.assertEqual('a', 'a')
        print '=========================================='

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()