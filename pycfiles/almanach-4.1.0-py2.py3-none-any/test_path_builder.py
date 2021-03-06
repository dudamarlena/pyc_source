# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/test/test_path_builder.py
# Compiled at: 2015-08-31 22:18:14
import alman, unittest

class TestPathBuilder(unittest.TestCase):

    class FakeResource(alman.apibits.ApiResource):
        _api_attributes = {'abc': ''}

        def __init__(self):
            super(TestPathBuilder.FakeResource, self).__init__({'abc': 'abc-value'})

    def setUp(self):
        self.params = {'dog': 'dog-value'}
        self.object = TestPathBuilder.FakeResource()

    def test_object_attributes(self):
        path = '/a/:abc/123'
        expected = '/a/abc-value/123'
        actual = alman.apibits.PathBuilder.build(self.object, None, path)
        self.assertEqual(expected, actual)
        return

    def test_param_values(self):
        path = '/a/:dog/123'
        expected = '/a/dog-value/123'
        actual = alman.apibits.PathBuilder.build(None, self.params, path)
        self.assertEqual(expected, actual)
        return

    def test_attributes_and_params(self):
        path = '/a/:dog/:abc/123'
        expected = '/a/dog-value/abc-value/123'
        actual = alman.apibits.PathBuilder.build(self.object, self.params, path)
        self.assertEqual(expected, actual)

    def test_missing_param(self):
        path = '/a/:dog/:abc/:cat/123'
        with self.assertRaises(ValueError):
            actual = alman.apibits.PathBuilder.build(self.object, self.params, path)