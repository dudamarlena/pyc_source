# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmcfarlane/dev/Chula/tests/unit/collection/test_restricted.py
# Compiled at: 2011-03-19 21:05:04
import copy, cPickle, unittest
from chula import collection, json
from chula.collection import restricted
from chula.error import *

class Human(collection.RestrictedCollection):

    def __validkeys__(self):
        return ('head', 'leg', 'arm', 'foot')

    def __deepcopy__(self, memo={}):
        """
        Return a fresh copy of a Collection object or subclass object
        """
        fresh = Human()
        for key, value in self.iteritems():
            fresh[key] = copy.deepcopy(value, memo)

        return fresh

    def __defaults__(self):
        self.head = 'wears hat'
        self.leg = 'two to walk with'
        self.arm = 'hold coffee with'
        self.foot = 'smell'


class Test_restricted_collection(unittest.TestCase):
    doctest = restricted

    def setUp(self):
        self.human = Human()

    def test_key_with_defalt(self):
        self.assertEquals(self.human.head, 'wears hat')
        self.assertEquals(self.human.foot, 'smell')

    def test_key_no_default(self):

        def simulate():

            class Human(collection.RestrictedCollection):

                def __validkeys__(self):
                    return ('head', 'stomach')

                def __defaults__(self):
                    self.head = 'wears hat'

            person = Human()

        self.assertRaises(RestrictecCollectionMissingDefaultAttrError, simulate)

    def test_get_invalid_attr(self):

        def simulate():
            return self.human.missing

        self.assertRaises(InvalidCollectionKeyError, simulate)

    def test_get_invalid_dict(self):

        def simulate():
            return self.human['missing']

        self.assertRaises(InvalidCollectionKeyError, simulate)

    def test_set_invalid_attr(self):

        def simulate():
            self.human.back = 'important'

        self.assertRaises(InvalidCollectionKeyError, simulate)

    def test_set_invalid_dict(self):

        def simulate():
            self.human['back'] = 'important'

        self.assertRaises(InvalidCollectionKeyError, simulate)

    def test_deepcopy(self):
        person = copy.deepcopy(self.human)
        self.assertEquals(person.head, 'wears hat')
        self.assertEquals(person.foot, 'smell')
        self.assertEquals(True, isinstance(person, collection.Collection))
        self.assertEquals(True, isinstance(person, collection.RestrictedCollection))

    def test_json_encoding(self):
        encoded = json.encode(self.human)
        decoded = json.decode(encoded)
        self.assertEquals(decoded['foot'], self.human.foot)
        self.assertEquals(decoded['head'], self.human.head)

    def test_cpickle_encoding(self):
        encoded = cPickle.dumps(self.human)
        decoded = cPickle.loads(encoded)
        self.assertEquals(decoded['foot'], self.human.foot)
        self.assertEquals(decoded['head'], self.human.head)