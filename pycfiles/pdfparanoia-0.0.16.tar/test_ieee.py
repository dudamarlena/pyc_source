# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kanzure/code/pdfparanoia/tests/test_ieee.py
# Compiled at: 2013-07-09 00:34:42
import unittest, pdfparanoia

class IEEEXploreTestCase(unittest.TestCase):

    def test_ieee(self):
        file_handler = open('tests/samples/ieee/9984106e01b63d996f19f383b8d96f02.pdf', 'rb')
        content = file_handler.read()
        self.assertIn('\n4 0 obj', content)
        self.assertIn('\n7 0 obj', content)
        output = pdfparanoia.plugins.IEEEXplore.scrub(content)
        self.assertNotIn('\n19 0 obj', output)
        self.assertNotIn('\n37 0 obj', output)
        self.assertNotIn('\n43 0 obj', output)
        self.assertNotIn('\n53 0 obj', output)
        self.assertNotIn('\n64 0 obj', output)
        self.assertNotIn('\n73 0 obj', output)