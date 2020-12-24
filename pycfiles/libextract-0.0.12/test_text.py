# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\rodrigo\github\libextract\tests\html\test_text.py
# Compiled at: 2015-04-09 00:01:44
from unittest import TestCase
from tests.html.test_commons import TestGetEtree
from libextract.html.article import get_node_length_pairs, node_text_length

class TestNodeTextLength(TestGetEtree):

    def runTest(self):
        res = self.etree.xpath('//body/article/div')
        for node in res:
            assert node_text_length(node) == 4

        assert res


class TestGetNodeLengthPairs(TestGetEtree):

    def runTest(self):
        u = list(get_node_length_pairs(self.etree))
        assert len(u) == 10
        for node, score in u:
            assert node.tag in {'article', 'body'}
            assert score in {4, 14}