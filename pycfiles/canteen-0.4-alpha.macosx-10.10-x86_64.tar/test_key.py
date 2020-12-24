# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen_tests/test_model/test_key.py
# Compiled at: 2014-09-26 04:50:19
"""

  model key tests
  ~~~~~~~~~~~~~~~

  tests canteen's model keys.

  :author: Sam Gammon <sg@samgammon.com>
  :copyright: (c) Sam Gammon, 2014
  :license: This software makes use of the MIT Open Source License.
            A copy of this license is included as ``LICENSE.md`` in
            the root of the project.

"""
from canteen import model
from canteen.model import Key
from canteen.model import exceptions
from canteen.model import AbstractKey
from canteen.test import FrameworkTest

class KeyTests(FrameworkTest):
    """ Tests `model.Key` and `model.AbstractKey`. """

    def test_construct_key(self):
        """ Test constructing a `Key` manually """
        k = Key('TestKind')
        self.assertEqual(k.kind, 'TestKind')
        k = Key('TestKind', 'sample')
        self.assertEqual(k.kind, 'TestKind')
        self.assertEqual(k.id, 'sample')
        pk = Key('TestParentKind', 'parent')
        k = Key('TestKind', 'child', parent=pk)
        self.assertEqual(k.kind, 'TestKind')
        self.assertEqual(k.id, 'child')
        self.assertEqual(k.parent, pk)
        self.assertEqual(k.__slots__, set())
        self.assertEqual(k.__class__.__name__, 'Key')
        self.assertEqual(k.__class__.__slots__, set())

    def test_key_inheritance(self):
        """ Test proper inheritance structure for `Key` """
        k = Key('TestKind', 'sample')
        self.assertIsInstance(k, Key)
        self.assertIsInstance(k, AbstractKey)
        self.assertIsInstance(k, object)
        self.assertTrue(issubclass(Key, AbstractKey))
        self.assertTrue(AbstractKey in Key.__bases__)
        self.assertIsInstance(Key, AbstractKey.__metaclass__)
        self.assertTrue(type(k) == Key)
        self.assertTrue(issubclass(Key, object))

    def test_key_stringify(self):
        """ Test string representation of a `Key` object """
        k = Key('SampleKind', 'sample_id')
        x = str(k)
        self.assertTrue('kind' in x)
        self.assertTrue('SampleKind' in x)
        self.assertTrue('id' in x)
        self.assertTrue('sample_id' in x)
        self.assertTrue('Key' in x)

    def test_key_class_stringify(self):
        """ Test the string representation of a `Key` class """
        x = str(Key)
        self.assertTrue('kind' in x)
        self.assertTrue('id' in x)
        self.assertTrue('Key' in x)

    def test_abstract_key(self):
        """ Test that `AbstractKey` works abstractly """
        with self.assertRaises(exceptions.AbstractConstructionFailure):
            AbstractKey()
        self.assertIsInstance(Key(), AbstractKey)

    def test_abstract_key_concrete(self):
        """ Test that `AbstractKey` works concretely """

        class SampleKey(AbstractKey):
            """ Tests subclasses of `AbstractKey`. """
            __schema__ = ('id', 'kind')

        self.assertTrue(SampleKey('Sample', 'id'))
        self.assertIsInstance(SampleKey('Sample', 'id'), Key)
        self.assertTrue(hasattr(SampleKey, '__schema__'))
        self.assertEqual(len(SampleKey.__schema__), 2)

    def test_key_concrete(self):
        """ Test that `Key` works concretely """

        class SampleKey(Key):
            """ Tests subclasses of `Key`. """
            __schema__ = ('id', 'kind')

        self.assertTrue(SampleKey('Sample', 'id'))
        self.assertIsInstance(SampleKey('Sample', 'id'), Key)
        self.assertTrue(hasattr(SampleKey, '__schema__'))
        self.assertEqual(len(SampleKey.__schema__), 2)

    def test_raw_key_format(self):
        """ Test constructing a key from a raw iterable """
        k = Key('Sample', 'sample')
        self.assertEqual(Key(raw=k.flatten()), k)
        self.assertEqual(Key.from_raw(k.flatten()), k)
        joined, struct = k.flatten(True)
        self.assertEqual(Key(raw=joined), k)
        self.assertEqual(Key.from_raw(joined), k)

    def test_urlsafe_key_format(self):
        """ Test constructing a key from its encoded form """
        k = Key('Sample', 'sample')
        self.assertEqual(Key(urlsafe=k.urlsafe()), k)
        self.assertEqual(Key.from_urlsafe(k.urlsafe()), k)

    def test_key_flatten(self):
        """ Test flattening a Key into a raw iterable """
        k = Key('Sample', 'sample')
        self.assertEqual(Key(raw=k.flatten()), k)
        self.assertEqual(Key.from_raw(k.flatten()), k)

    def test_key_nonzero(self):
        """ Test nonzero functionality in a key """
        k, nk = Key('Sample'), Key('Sample', 'sample')
        self.assertTrue(nk)
        self.assertTrue(not k)

    def test_key_len(self):
        """ Test length of a `Key`, which should be 0 for an incomplete key """
        k, nk = Key('Sample'), Key('Sample', 'sample')
        self.assertEqual(len(k), 0)
        self.assertEqual(len(nk), 1)

    def test_key_with_model_class_kind(self):
        """ Test making a `Key` via using a model class as the kind """

        class KindedModel(model.Model):
            """ Sample for testing key creation from model classes. """
            string = basestring

        k1 = model.Key('KindedModel', 'test_id')
        k2 = model.Key(KindedModel, 'test_id')
        ko = model.Key(KindedModel)
        self.assertEqual(k1.kind, 'KindedModel')
        self.assertEqual(k1.id, 'test_id')
        self.assertEqual(k2.kind, k1.kind)
        self.assertEqual(ko.kind, k1.kind)
        self.assertEqual(k2.id, k2.id)

    def test_key_ancestry(self):
        """ Test `Key` ancestry mechanisms """
        pk = model.Key('ParentKind', 'parent_id')
        ck = model.Key('ChildKind', 'child_id', parent=pk)
        gk = model.Key('GrandchildKind', 'grandchild_id', parent=ck)
        ggk = model.Key('GreatGrandchildKind', 'great_grandchild_id', parent=gk)
        self.assertEqual(pk.parent, None)
        self.assertEqual(ck.parent, pk)
        self.assertEqual(gk.parent, ck)
        self.assertEqual(ggk.parent, gk)
        pk_ancestry = [ i for i in pk.ancestry ]
        ck_ancestry = [ i for i in ck.ancestry ]
        gk_ancestry = [ i for i in gk.ancestry ]
        ggk_ancestry = [ i for i in ggk.ancestry ]
        self.assertEqual(len(pk_ancestry), 1)
        self.assertEqual(len(ck_ancestry), 2)
        self.assertEqual(len(gk_ancestry), 3)
        self.assertEqual(len(ggk_ancestry), 4)
        self.assertEqual(len(pk), 1)
        self.assertEqual(len(ck), 2)
        self.assertEqual(len(gk), 3)
        self.assertEqual(len(ggk), 4)
        for k in (pk, ck, gk, ggk):
            self.assertTrue(k)

        return

    def test_key_with_overflowing_schema(self):
        """ Test construction of a `Key` with too many schema items """
        with self.assertRaises(TypeError):
            model.Key(*('SampleKind', 'id', 'coolstring', 'whatdowedo', 'whenwehave',
                        'thismanyarguments'))

    def test_key_construct_multiple_formats(self):
        """ Test constuction of a `Key` with multiple formats """
        ok = model.Key('Sample', 'sample_id')
        with self.assertRaises(TypeError):
            model.Key(raw=ok.flatten(False)[1], urlsafe=ok.urlsafe())

    def test_key_auto_id(self):
        """ Test an integer-based ID field """

        class AutoincrementTest(model.Model):
            """ Test that keys autoincrement properly when not assigned
        deterministic name values. """
            message = (
             basestring, {'default': 'Hello, world!'})

        a = AutoincrementTest(key=model.Key(AutoincrementTest.kind(), 'testing-string-key'))
        dk = a.put()
        nk = AutoincrementTest().put()
        nk2 = AutoincrementTest().put()
        self.assertIsInstance(nk.id, int)
        self.assertIsInstance(dk.id, basestring)
        self.assertTrue(nk2.id > nk.id)

    def test_key_adapter(self):
        """ Test that the adapter is attached correctly to `Key` """
        k = model.Key('TestKind', 'test')
        self.assertTrue(hasattr(model.Key, '__adapter__'))
        self.assertIsInstance(model.Key.__adapter__, model.adapter.ModelAdapter)
        self.assertTrue(hasattr(k, '__adapter__'))
        self.assertIsInstance(model.Key.__adapter__, model.adapter.ModelAdapter)

    def test_key_equality(self):
        """ Test that keys equal each other when they should """
        conditions = []
        k1 = model.Key('TestKind', 'blabs')
        k2 = model.Key('TestKind', 'blabs')
        conditions.append(k1 == k2)
        k3 = model.Key('TestKind')
        k4 = model.Key('TestKind')
        conditions.append(k3 == k4)
        k5 = model.Key('TestSubkind', 'blobs', parent=k1)
        k6 = model.Key('TestSubkind', 'blobs', parent=k2)
        conditions.append(k5 == k6)
        [ self.assertTrue(condition) for condition in conditions ]

    def test_key_inequality(self):
        """ Test that keys don't equal each other when they shouldn't """
        conditions = []
        k1 = model.Key('TestKind', 'blabs')
        k2 = model.Key('TestKind', 'blobs')
        conditions.append(k1 != k2)
        k3 = model.Key('TestKind')
        k4 = model.Key('TestOtherKind')
        conditions.append(k3 != k4)
        k5 = model.Key('TestSubkind', 'blabs', parent=k1)
        k6 = model.Key('TestSubkind', 'blobs', parent=k1)
        conditions.append(k5 != k6)
        k7 = model.Key('TestSubkindOne', 'blabs', parent=k1)
        k8 = model.Key('TestSubkindTwo', 'blabs', parent=k1)
        conditions.append(k7 != k8)
        k9 = model.Key('TestSubkind', 'blabs', parent=k1)
        k10 = model.Key('TestSubkind', 'blabs', parent=k2)
        conditions.append(k9 != k10)
        [ self.assertTrue(condition) for condition in conditions ]

    def test_key_format(self):
        """ Test format specification on `Key` """
        k1 = model.Key('Test', 'testkey')
        self.assertTrue(hasattr(model.Key, '__schema__'))
        self.assertIsInstance(model.Key.__schema__, tuple)
        self.assertTrue(len(model.Key.__schema__) > 1)
        self.assertTrue(hasattr(k1, '__schema__'))
        self.assertIsInstance(model.Key.__schema__, tuple)
        self.assertTrue(len(model.Key.__schema__) > 1)

    def test_key_set_unknown_attribute(self):
        """ Test setting an unknown and known attribute on a `Key` """
        k = model.Key('CoolKind', 'coolid')
        with self.assertRaises(AttributeError):
            k.blabble = True

    def test_key_overwrite_known_attribute(self):
        """ Test overwriting a known (schema-d) attribute on a `Key` """
        k = model.Key('CoolKind', 'coolid')
        with self.assertRaises(AttributeError):
            k.kind = 'MyKind'
        with self.assertRaises(AttributeError):
            k.id = 10

    def test_key_set_attribute_persisted(self):
        """ Test setting a valid attribute on a persisted `Key` """

        class PersistedKeyTest(model.Model):
            """ Test model for making sure writing to a persisted key fails. """
            message = (
             basestring, {'default': 'Hello, world!'})

        with self.assertRaises(AttributeError):
            k = PersistedKeyTest().put()
            k.id = 5
        with self.assertRaises(AttributeError):
            k = PersistedKeyTest().put()
            k._set_internal('kind', 'Blabs')
        with self.assertRaises(AttributeError):
            k = PersistedKeyTest().put()
            k._set_internal('id', 25)