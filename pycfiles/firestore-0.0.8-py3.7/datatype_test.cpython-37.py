# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/datatypes/datatype_test.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 490 bytes
from unittest import TestCase
from firestore import Collection, Datatype
from firestore.errors import ValidationError

class DatatypeDoc(Collection):
    first_name = Datatype('sTring', required=True, coerce=False)


class DatatypeTest(TestCase):

    def setUp(self):
        self.dd = DatatypeDoc()

    def tearDown(self):
        pass

    def test_datatype_returns_appropriate_field_type(self):
        with self.assertRaises(ValueError):
            self.dd.first_name = 5