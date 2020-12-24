# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/datatypes/boolean_test.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 548 bytes
from unittest import TestCase
from firestore import Boolean, Collection
from firestore.containers.collection import Cache

class BooleanDocument(Collection):
    is_verified = Boolean(default=False, required=False)


class BooleanTest(TestCase):

    def setUp(self):
        self.bd = BooleanDocument()

    def tearDown(self):
        pass

    def test_boolean_in_document_instance(self):
        self.bd.is_verified = True
        expected = Cache()
        expected.add('is_verified', True)
        self.assertEqual(expected, self.bd._data)