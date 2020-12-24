# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/current/json_tests/test_recursion.py
# Compiled at: 2019-06-26 11:58:00
from unittest import TestCase
from pyutil import jsonutil as json

class JSONTestObject:
    pass


class RecursiveJSONEncoder(json.JSONEncoder):
    recurse = False

    def default(self, o):
        if o is JSONTestObject:
            if self.recurse:
                return [JSONTestObject]
            else:
                return 'JSONTestObject'

        return json.JSONEncoder.default(o)


class TestRecursion(TestCase):

    def test_listrecursion(self):
        x = []
        x.append(x)
        try:
            json.dumps(x)
        except ValueError:
            pass
        else:
            self.fail("didn't raise ValueError on list recursion")

        x = []
        y = [
         x]
        x.append(y)
        try:
            json.dumps(x)
        except ValueError:
            pass
        else:
            self.fail("didn't raise ValueError on alternating list recursion")

        y = []
        x = [
         y, y]
        json.dumps(x)

    def test_dictrecursion(self):
        x = {}
        x['test'] = x
        try:
            json.dumps(x)
        except ValueError:
            pass
        else:
            self.fail("didn't raise ValueError on dict recursion")

        x = {}
        {'a': x, 'b': x}
        json.dumps(x)

    def test_defaultrecursion(self):
        enc = RecursiveJSONEncoder()
        self.assertEqual(enc.encode(JSONTestObject), '"JSONTestObject"')
        enc.recurse = True
        try:
            enc.encode(JSONTestObject)
        except ValueError:
            pass
        else:
            self.fail("didn't raise ValueError on default recursion")