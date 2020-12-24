# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sparrow/tests/test_dict_format.py
# Compiled at: 2009-07-20 09:57:48
from unittest import TestCase, TestSuite, makeSuite, main
from StringIO import StringIO
from sparrow.utils import ntriples_to_dict, dict_to_ntriples

class DictFormatTest(TestCase):

    def test_uri_object(self):
        nt = '<uri:a> <uri:b> <uri:c> .\n'
        data = ntriples_to_dict(StringIO(nt))
        self.assertEquals(data, {'uri:a': {'uri:b': [
                             {'value': 'uri:c', 'type': 'uri'}]}})
        self.assertEquals(nt, dict_to_ntriples(data).read())

    def test_bnode_object(self):
        nt = '<uri:a> <uri:b> _:c .\n'
        data = ntriples_to_dict(StringIO(nt))
        self.assertEquals(data, {'uri:a': {'uri:b': [
                             {'value': 'c', 'type': 'bnode'}]}})
        self.assertEquals(nt, dict_to_ntriples(data).read())

    def test_bnode_subject(self):
        nt = '_:a <uri:b> _:c .\n'
        data = ntriples_to_dict(StringIO(nt))
        self.assertEquals(data, {'_:a': {'uri:b': [
                           {'value': 'c', 'type': 'bnode'}]}})
        self.assertEquals(nt, dict_to_ntriples(data).read())

    def test_literal_object(self):
        nt = '<uri:a> <uri:b> "foo" .\n'
        data = ntriples_to_dict(StringIO(nt))
        self.assertEquals(data, {'uri:a': {'uri:b': [
                             {'value': 'foo', 'type': 'literal'}]}})
        self.assertEquals(nt, dict_to_ntriples(data).read())

    def test_literal_language_object(self):
        nt = '<uri:a> <uri:b> "foo"@en .\n'
        data = ntriples_to_dict(StringIO(nt))
        self.assertEquals(data, {'uri:a': {'uri:b': [
                             {'value': 'foo', 'lang': 'en', 
                                'type': 'literal'}]}})
        self.assertEquals(nt, dict_to_ntriples(data).read())

    def test_literal_datatype_object(self):
        nt = '<uri:a> <uri:b> "foo"^^<uri:string> .\n'
        data = ntriples_to_dict(StringIO(nt))
        self.assertEquals(data, {'uri:a': {'uri:b': [
                             {'value': 'foo', 'datatype': 'uri:string', 
                                'type': 'literal'}]}})
        self.assertEquals(nt, dict_to_ntriples(data).read())

    def test_literal_value_quote_escape(self):
        nt = '<uri:a> <uri:b> "I say \\"Hello\\"." .\n'
        data = ntriples_to_dict(StringIO(nt))
        self.assertEquals(data, {'uri:a': {'uri:b': [
                             {'value': 'I say "Hello".', 'type': 'literal'}]}})
        self.assertEquals(nt, dict_to_ntriples(data).read())

    def test_literal_value_backslash_escape(self):
        nt = '<uri:a> <uri:b> "c:\\\\temp\\\\foo.txt" .\n'
        data = ntriples_to_dict(StringIO(nt))
        self.assertEquals(data, {'uri:a': {'uri:b': [
                             {'value': 'c:\\temp\\foo.txt', 'type': 'literal'}]}})
        self.assertEquals(nt, dict_to_ntriples(data).read())

    def test_literal_value_newline_tab_escape(self):
        nt = '<uri:a> <uri:b> "\\n\\tHello!\\n" .\n'
        data = ntriples_to_dict(StringIO(nt))
        self.assertEquals(data, {'uri:a': {'uri:b': [
                             {'value': '\n\tHello!\n', 'type': 'literal'}]}})
        self.assertEquals(nt, dict_to_ntriples(data).read())


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(DictFormatTest))
    return suite


if __name__ == '__main__':
    main(defaultTest='test_suite')