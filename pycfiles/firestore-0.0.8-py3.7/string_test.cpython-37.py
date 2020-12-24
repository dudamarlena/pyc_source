# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/datatypes/string_test.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 1348 bytes
from unittest import TestCase
from firestore import Collection, String
from firestore.errors import ValidationError
from firestore.containers.collection import Cache

class StringDocument(Collection):
    name = String(required=True, minimum=5, maximum=10)
    email = String(coerce=False)


class OptionsDocument(Collection):
    name = String(options=('You', 'There'))


class StringTest(TestCase):
    __doc__ = '\n    Tests for the String firestore datatype/field class\n    '

    def setUp(self):
        self.sd = StringDocument()
        self.od = OptionsDocument()

    def tearDown(self):
        pass

    def test_string_minimum(self):
        with self.assertRaises(ValidationError):
            self.sd.name = 'me'
        with self.assertRaises(ValidationError):
            self.sd.name = 'very very very very long name'
        with self.assertRaises(ValidationError):
            self.sd.name = 5

    def test_string_coerce(self):
        with self.assertRaises(ValueError):
            self.sd.email = 5

    def test_options_error(self):
        with self.assertRaises(ValidationError):
            self.od.name = 'Haba'

    def test_string_in_collection_document(self):
        self.sd.name = 'Whosand'
        expecting = Cache()
        expecting.add('name', 'Whosand')
        self.assertEqual(expecting, self.sd._data)