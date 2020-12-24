# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/datatypes/timestamp_test.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 1525 bytes
from unittest import TestCase
from datetime import timedelta, timezone, datetime as clock
from firestore import Collection, Integer, String, Timestamp
from firestore.containers.collection import Cache
from firestore.errors import ValidationError

class TimestampDocument(Collection):
    created_date = Timestamp(default=(clock.now))
    last_modified = Timestamp(minimum='2019-10-20')
    active_until = Timestamp(maximum='2020')
    expiry_date = Timestamp(minimum=1609459200)

    def do_nothin_special(self):
        """"""
        pass


class TimestampTest(TestCase):

    def setUp(self):
        self.td = TimestampDocument()
        self._ = clock.now(tz=(timezone.utc))

    def tearDown(self):
        pass

    def test_timestamp_in_collection_document(self):
        self.td.created_date = self._
        expected = Cache()
        expected.add('created_date', self._)
        self.assertEqual(expected, self.td._data)

    def test_only_valid_types_allowed(self):
        with self.assertRaises(ValueError):
            self.td.created_date = 'you'

    def test_coerces_minimum_and_still_raises_error(self):
        with self.assertRaises(ValidationError):
            self.td.last_modified = '2019-10-19'
        with self.assertRaises(ValidationError):
            self.td.expiry_date = '2017'

    def test_coerces_maximum_and_still_raises_error(self):
        with self.assertRaises(ValidationError):
            self.td.active_until = 1609459200.28904