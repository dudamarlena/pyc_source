# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kanzure/code/pdfparanoia/tests/test_rsc.py
# Compiled at: 2013-07-09 00:34:42
import unittest, pdfparanoia

class RoyalSocietyOfChemistryTestCase(unittest.TestCase):

    def test_rsc(self):
        file_handler = open('tests/samples/rsc/3589bf649f8bb019bd97be9880627b7c.pdf', 'rb')
        content = file_handler.read()
        file_handler.close()
        self.assertIn('pubs.rsc.org', content)
        output = pdfparanoia.plugins.RoyalSocietyOfChemistry.scrub(content)
        self.assertIn('pubs.rsc.org', output)