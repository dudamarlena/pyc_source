# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\rodrigo\github\libextract\tests\html\test_commons.py
# Compiled at: 2015-04-09 00:01:44
from unittest import TestCase
from tests import asset_path
from libextract.html import parse_html
FOO_ASSET = asset_path('full_of_foos.html')

class TestGetEtree(TestCase):

    def setUp(self):
        with open(FOO_ASSET, 'rb') as (fp):
            self.etree = parse_html(fp)

    def runTest(self):
        divs = self.etree.xpath('//body/article/div')
        assert all(k.text == 'foo.' for k in divs)
        assert len(divs) == 9