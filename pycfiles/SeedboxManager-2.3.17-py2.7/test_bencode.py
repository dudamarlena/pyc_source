# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/tests/torrent/test_bencode.py
# Compiled at: 2015-06-14 13:30:57
"""Test class for benecode

* example values partially taken from http://en.wikipedia.org/wiki/Bencode
* test case inspired by Mark Pilgrim's examples:
        http://diveintopython.org/unit_testing/romantest.html
"""
from seedbox.tests import test
from seedbox.torrent import bencode

class KnownValues(test.BaseTestCase):
    knownValues = (
     (0, 'i0e'),
     (1, 'i1e'),
     (10, 'i10e'),
     (42, 'i42e'),
     (-42, 'i-42e'),
     (
      True, 'i1e'),
     (
      False, 'i0e'),
     ('spam', '4:spam'),
     ('parrot sketch', '13:parrot sketch'),
     (
      [
       'parrot sketch', 42], 'l13:parrot sketchi42ee'),
     (
      {'foo': 42, 'bar': 'spam'},
      'd3:bar4:spam3:fooi42ee'))

    def test_bencode_known_values(self):
        for plain, encoded in self.knownValues:
            result = bencode.bencode(plain)
            self.assertEqual(encoded, result)

    def test_bdecode_known_values(self):
        for plain, encoded in self.knownValues:
            result = bencode.bdecode(encoded)
            self.assertEqual(plain, result)

    def test_roundtrip_encoded(self):
        for plain, encoded in self.knownValues:
            result = bencode.bdecode(encoded)
            self.assertEqual(encoded, bencode.bencode(result))

    def test_roundtrip_decoded(self):
        for plain, encoded in self.knownValues:
            result = bencode.bencode(plain)
            self.assertEqual(plain, bencode.bdecode(result))


class IllegaleValues(test.BaseTestCase):

    def test_nonstrings_raise_illegal_input_for_decode(self):
        self.assertRaises(bencode.BTFailure, bencode.bdecode, [0])
        self.assertRaises(bencode.BTFailure, bencode.bdecode, None)
        self.assertRaises(bencode.BTFailure, bencode.bdecode, [1, 2])
        self.assertRaises(bencode.BTFailure, bencode.bdecode, {'foo': 'bar'})
        return

    def test_raise_illegal_input_for_decode(self):
        self.assertRaises(bencode.BTFailure, bencode.bdecode, 'foo')
        self.assertRaises(bencode.BTFailure, bencode.bdecode, 'x:foo')
        self.assertRaises(bencode.BTFailure, bencode.bdecode, 'x42e')


class Dictionaries(test.BaseTestCase):

    def test_sorted_keys_for_dicts(self):
        adict = {'zoo': 42, 'bar': 'spam'}
        encoded_dict = bencode.bencode(adict)
        self.assertTrue(encoded_dict.index('zoo') > encoded_dict.index('bar'))

    def test_nested_dictionary(self):
        adict = {'foo': 42, 'bar': {'sketch': 'parrot', 'foobar': 23}}
        encoded_dict = bencode.bencode(adict)
        self.assertEqual(encoded_dict, 'd3:bard6:foobari23e6:sketch6:parrote3:fooi42ee')