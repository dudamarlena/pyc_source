# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mortar/tests/test_field.py
# Compiled at: 2008-12-19 12:41:15
import unittest
from mortar import content, types
from testfixtures import should_raise, compare
from zope.interface.verify import verifyObject

class FieldTests(unittest.TestCase):

    def setUp(self):
        self.content = content()
        self.field = self.content['test']

    def test_interface(self):
        from mortar.interfaces import IField
        verifyObject(IField, self.field)

    def test_get_simple(self):
        self.field.set('value')
        self.assertEqual(self.field.get('name'), 'value')

    def test_get_default_no_default(self):
        self.assertEqual(self.field.get(), None)
        return

    def test_get_default_default_supplied(self):
        self.assertEqual(self.field.get(default='123'), '123')

    def test_type_simple(self):
        self.field.set('value')
        self.failUnless(self.field.type is types.text)

    def test_get_type_not_there(self):
        self.failUnless(self.field.type is None)
        return

    def test_delete(self):
        self.assertEqual(self.content.names, [])
        self.field.set('x')
        self.assertEqual(self.content.names, ['test'])
        self.field.delete()
        self.assertEqual(self.content.names, [])

    def test_delete_not_there(self):
        self.assertEqual(self.content.names, [])
        should_raise(self.field.delete, KeyError('test'))()
        self.assertEqual(self.content.names, [])


class TestSet(unittest.TestCase):
    method = 'set'

    def setUp(self):
        self.content = content()
        self.field = self.content['test']

    def check(self, e_value, e_type, *args, **kw):
        getattr(self.field, self.method)(*args, **kw)
        self.assertEqual(e_value, self.field.get())
        self.assertEqual(e_type, self.field.type)

    def test_default(self):
        self.check('value', types.text, 'value')

    def test_default_non_string(self):
        self.check(1, types.number, 1)

    def test_coerce_to_texts(self):
        self.check(('value', ), types.texts, 'value', type=types.texts)

    def test_coerce_to_None(self):
        self.check(None, None, ())
        return


class TestAdd(TestSet):
    method = 'add'

    def test_default(self):
        self.check(['value'], types.texts, 'value')

    def test_default_non_string(self):
        self.check([1], types.numbers, 1)

    def test_coerce_to_texts(self):
        self.check(['value'], types.texts, 'value', type=types.texts)

    def test_add_to_existing(self):
        self.field.set('test1')
        self.field.add('test2')
        compare(self.field.get(), ['test1', 'test2'])

    def test_add_wrong_type_attempt(self):
        self.field.set('test1')
        should_raise(self.field.add, TypeError("Can't add number to texts"))(1)

    def test_add_wrong_type_sequence_attempt(self):
        self.field.set('test1')
        should_raise(self.field.add, TypeError("Can't add numbers to texts"))((1, ))

    def test_add_list_to_existing(self):
        self.field.set('test1')
        self.field.add(['test2'])
        compare(self.field.get(), ['test1', 'test2'])

    def test_add_tuple_to_existing(self):
        self.field.set('test1')
        self.field.add(('test2', ))
        compare(self.field.get(), ['test1', 'test2'])


def test_suite():
    return unittest.TestSuite((
     unittest.makeSuite(FieldTests),
     unittest.makeSuite(TestSet),
     unittest.makeSuite(TestAdd)))