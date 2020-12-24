# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kanzure/code/pdfparanoia/tests/test_jstor.py
# Compiled at: 2013-07-09 00:34:42
import unittest, pdfparanoia

class JSTORTestCase(unittest.TestCase):

    def test_jstor(self):
        file_handler = open('tests/samples/jstor/231a515256115368c142f528cee7f727.pdf', 'rb')
        content = file_handler.read()
        file_handler.close()
        self.assertIn('\n18 0 obj \n', content)
        self.assertIn('\n19 0 obj \n', content)
        output = pdfparanoia.plugins.JSTOR.scrub(content)
        self.assertIn('\n19 0 obj\n<</Length 2862>>stream', output)