# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\rodrigo\github\libextract\libextract\tests\test_formatters.py
# Compiled at: 2015-04-09 22:35:58
from copy import deepcopy
from unittest import TestCase
from lxml import etree
from libextract.formatters import node_json

class TestNodeJson(TestCase):

    def setUp(self):
        self.etree = etree.fromstring('<html class="this those" id="that"><p>Hello World</p></html>')
        self.expected_json = {'children': None, 
           'xpath': '/html', 
           'class': [
                   'this', 'those'], 
           'text': None, 
           'tag': 'html', 
           'id': [
                'that']}
        return

    def test_simple(self):
        assert node_json(self.etree) == self.expected_json

    def test_depth(self):
        self.expected_json['children'] = [
         {'children': None, 
            'xpath': '/html/p', 
            'text': 'Hello World', 
            'class': [], 'id': [], 'tag': 'p'}]
        expected = deepcopy(self.expected_json)
        expected['children'][0]['children'] = []
        assert node_json(self.etree, depth=1) == self.expected_json
        assert node_json(self.etree, depth=2) == expected
        return