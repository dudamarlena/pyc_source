# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alexhall/Dropbox/jsonfinder/jsonfinder/tests/test.py
# Compiled at: 2015-03-27 03:32:10
import json, unittest
from jsonfinder import *
from jsonfinder import check_min_elements

class BasicTests(unittest.TestCase):

    def setUp(self):
        with open('tests/testin.txt') as (infile):
            self.string = infile.read()

    def test_finder(self):
        result = []
        for start, end, obj in jsonfinder(self.string):
            if obj is not None:
                result.append(json.dumps(obj, indent=2, sort_keys=True))
            else:
                result.append(self.string[start:end])

        with open('tests/testout.txt') as (outfile):
            self.assertEquals(('\n').join(result), outfile.read())
        return

    def test_has_json(self):
        self.assertTrue(has_json(self.string))
        self.assertTrue(has_json('hi { [1] stuff'))
        self.assertFalse(has_json('hi { [1,] stuff'))
        self.assertFalse(has_json('a normal string'))
        self.assertFalse(has_json(''))

    def test_only_json(self):
        self.assertRaises(ValueError, lambda : only_json(self.string))
        self.assertEquals(only_json('prefix {"a":"b"} suffix'), (7, 16, {'a': 'b'}))
        self.assertEquals(only_json('true }{ {{ true }} [1,2,3] false 1 2 3 null'), (19, 26, [1, 2, 3]))

    def test_type_error(self):
        self.assertRaises(AttributeError, lambda : has_json(123))

    def test_start_end_match(self):
        prev = 0
        end = None
        for start, end, obj in jsonfinder(self.string):
            self.assertEquals(start, prev)
            prev = end

        self.assertEquals(end, len(self.string))
        return

    def test_empty_object(self):
        self.assertFalse(any(t[2] for t in jsonfinder('{}')))
        self.assertEquals(len(list(jsonfinder('{}'))), 3)

    def test_min_elemets(self):
        obj = {'a': [1, 2], 'b': [3, [4, {'c': 5, 'd': [6, 7, [8], {'e': 9}]}, 10]]}
        size = 10
        for test_size in xrange(size * 2):
            self.assertEquals(check_min_elements(obj, test_size), test_size <= size)


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(BasicTests))
import jsonfinder as package, doctest
suite.addTest(doctest.DocTestSuite(package))
unittest.TextTestRunner(verbosity=1).run(suite)