# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/dep/_simplejson/tests/test_check_circular.py
# Compiled at: 2011-01-13 01:48:00
from unittest import TestCase
import simplejson as json

def default_iterable(obj):
    return list(obj)


class TestCheckCircular(TestCase):

    def test_circular_dict(self):
        dct = {}
        dct['a'] = dct
        self.assertRaises(ValueError, json.dumps, dct)

    def test_circular_list(self):
        lst = []
        lst.append(lst)
        self.assertRaises(ValueError, json.dumps, lst)

    def test_circular_composite(self):
        dct2 = {}
        dct2['a'] = []
        dct2['a'].append(dct2)
        self.assertRaises(ValueError, json.dumps, dct2)

    def test_circular_default(self):
        json.dumps([set()], default=default_iterable)
        self.assertRaises(TypeError, json.dumps, [set()])

    def test_circular_off_default(self):
        json.dumps([set()], default=default_iterable, check_circular=False)
        self.assertRaises(TypeError, json.dumps, [set()], check_circular=False)