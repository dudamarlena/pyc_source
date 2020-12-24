# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/uche/dev/amara/test/pushtree/test_pushtree.py
# Compiled at: 2011-01-13 14:24:43
import amara
from amara.pushtree import pushtree
from amara.lib import treecompare
from cStringIO import StringIO
XMLDECL = '<?xml version="1.0" encoding="UTF-8"?>\n'
XML1 = '<doc>\n  <one><a>0</a><a>1</a></one>\n  <two><a>10</a><a>11</a></two>\n</doc>'
XML2 = '<doc xmlns="urn:bogus:x">\n  <one><a>0</a><a>1</a></one>\n  <two><a>10</a><a>11</a></two>\n</doc>'
XML3 = '<x:doc xmlns:x="urn:bogus:x">\n  <x:one><x:a>0</x:a><x:a>1</x:a></x:one>\n  <x:two><x:a>10</x:a><x:a>11</x:a></x:two>\n</x:doc>'
XML4 = '<doc xmlns:x="urn:bogus:x">\n  <one><x:a>0</x:a><x:a>1</x:a></one>\n  <two><a>10</a><a>11</a></two>\n</doc>'

def test_1():
    EXPECTED = [
     '<a>0</a>', '<a>1</a>', '<a>10</a>', '<a>11</a>']
    results = []

    def callback(node):
        results.append(node)

    pushtree(XML1, 'a', callback)
    for (result, expected) in zip(results, EXPECTED):
        treecompare.check_xml(result.xml_encode(), XMLDECL + expected)


def test_2():
    EXPECTED = [
     '<a xmlns="urn:bogus:x">0</a>', '<a xmlns="urn:bogus:x">1</a>', '<a xmlns="urn:bogus:x">10</a>', '<a xmlns="urn:bogus:x">11</a>']
    results = []

    def callback(node):
        results.append(node)

    pushtree(XML2, 'a', callback, namespaces={None: 'urn:bogus:x'})
    for (result, expected) in zip(results, EXPECTED):
        treecompare.check_xml(result.xml_encode(), XMLDECL + expected)

    return


def test_3():
    EXPECTED = [
     '<x:a xmlns:x="urn:bogus:x">0</x:a>', '<x:a xmlns:x="urn:bogus:x">1</x:a>', '<x:a xmlns:x="urn:bogus:x">10</x:a>', '<x:a xmlns:x="urn:bogus:x">11</x:a>']
    results = []

    def callback(node):
        results.append(node)

    pushtree(XML3, 'x:a', callback, namespaces={'x': 'urn:bogus:x'})
    for (result, expected) in zip(results, EXPECTED):
        treecompare.check_xml(result.xml_encode(), XMLDECL + expected)


def test_4():
    EXPECTED = [
     '<x:a xmlns:x="urn:bogus:x">0</x:a>', '<x:a xmlns:x="urn:bogus:x">1</x:a>']
    results = []

    def callback(node):
        results.append(node)

    pushtree(XML4, 'x:a', callback, namespaces={'x': 'urn:bogus:x'})
    for (result, expected) in zip(results, EXPECTED):
        treecompare.check_xml(result.xml_encode(), XMLDECL + expected)


testdoc = "    <a xmlns:x='http://spam.com/'>\n    <?xml-stylesheet href='mystyle.css' type='text/css'?>\n    <blah>\n    <x:a b='2'></x:a>\n    </blah>\n    <c d='3'/>\n    </a>\n    "
import unittest

class TestPushTree(unittest.TestCase):

    def setUp(self):
        self.results = []
        self.infile = StringIO(testdoc)

    def tearDown(self):
        del self.results[:]

    def callback(self, node):
        self.results.append(node)

    def testsimpleelement(self):
        pushtree(self.infile, 'a', self.callback)
        self.assertEquals(len(self.results), 2)
        expected_names = [
         ('http://spam.com/', 'a'),
         (None, 'a')]
        for (node, ename) in zip(self.results, expected_names):
            self.assertEquals(node.xml_name, ename)

        return

    def testnestedelement(self):
        pushtree(self.infile, 'a/c', self.callback)
        self.assertEquals(len(self.results), 1)
        self.assertEquals(self.results[0].xml_name, (None, 'c'))
        return

    def testattribute(self):
        pushtree(self.infile, 'a/*/*/@b', self.callback)
        self.assertEquals(len(self.results), 1)
        self.assertEquals(self.results[0].xml_name, ('http://spam.com/', 'a'))

    def testnamespaces(self):
        pushtree(self.infile, '/a//q:a', self.callback, namespaces={'q': 'http://spam.com/'})
        self.assertEquals(len(self.results), 1)
        self.assertEquals(self.results[0].xml_name, ('http://spam.com/', 'a'))


TREE1 = "\n<a x='1'>\n  <b x='2'>\n    <c x='3'>\n      <b x='4'>\n        <d x='5' />\n        <e x='6' />\n        <d x='7' />\n        <b x='8' />\n        <c x='9' />\n      </b>\n      <c x='10'><c x='11' /></c>\n    </c>\n  </b>\n</a>\n"
TREEDOC = amara.parse(TREE1)

class TestXPathMatcher(unittest.TestCase):

    def setUp(self):
        self.results = []
        self.infile = StringIO(testdoc)

    def tearDown(self):
        del self.results[:]

    def callback(self, node):
        self.results.append(node.xml_attributes['x'])

    def compare_matches(self, xpath):
        del self.results[:]
        select_ids = set(node.xml_attributes['x'] for node in TREEDOC.xml_select('//' + xpath))
        pushtree(TREE1, xpath, self.callback)
        push_ids = set(self.results)
        self.assertEquals(select_ids, push_ids)

    def test_relative_single(self):
        self.compare_matches('a')
        self.compare_matches('b')
        self.compare_matches('c')


def test_predicate1():
    EXPECTED = [
     '<a>0</a>', '<a>1</a>', '<a>10</a>', '<a>11</a>']
    results = []

    def callback(node):
        results.append(node)

    pushtree(TREE1, "b[x='4']", callback)
    for (result, expected) in zip(results, EXPECTED):
        treecompare.check_xml(result.xml_encode(), XMLDECL + expected)


if __name__ == '__main__':
    unittest.main()