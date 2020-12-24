# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /beanbag_licensing/tests/test_immutable.py
# Compiled at: 2019-06-17 15:11:31
"""Unit tests for beanbag_licensing.immutable."""
from __future__ import unicode_literals
from djblets.testing.testcases import TestCase
from beanbag_licensing import immutable as immutable_module
from beanbag_licensing.immutable import _ImmutableMixin, immutable
ImmutableMetaClass = getattr(immutable_module, b'__ImmutableMetaClass')
ImmutableAttrsMetaClass = ImmutableMetaClass.__bases__[0]

class ImmutableMixinTests(TestCase):
    """Unit tests for beanbag_licensing.immutable._ImmutableMixin."""

    def test_class_state(self):
        """Testing _ImmutableMixin class state"""
        self.assertFalse(hasattr(_ImmutableMixin, b'__metaclass__'))
        self.assertEqual(_ImmutableMixin.__bases__, (object,))

    def test_delete_class_attr(self):
        """Testing _ImmutableMixin and deleting class attributes fails"""
        with self.assertRaises(AttributeError):
            del _ImmutableMixin.__setattr__
        with self.assertRaises(AttributeError):
            delattr(_ImmutableMixin, b'__setattr__')
        with self.assertRaises(AttributeError):
            del _ImmutableMixin.new_var
        with self.assertRaises(TypeError):
            del _ImmutableMixin.__dict__[b'__setattr__']

    def test_set_class_attr(self):
        """Testing _ImmutableMixin and setting class attributes fails"""
        with self.assertRaises(AttributeError):
            _ImmutableMixin.__setattr__ = lambda *args: None
        with self.assertRaises(AttributeError):
            setattr(_ImmutableMixin, b'__setattr__', lambda *args: None)
        with self.assertRaises(AttributeError):
            _ImmutableMixin.new_var = lambda *args: None
        with self.assertRaises(TypeError):
            _ImmutableMixin.__dict__[b'__setattr__'] = lambda *args: None

    def test_subclass_init(self):
        """Testing _ImmutableMixin subclass and construction/initialization"""

        @immutable
        class MyClass(object):
            immutable_attrs = ('a', 'b')
            mutable_attrs = ('c', )

            def __init__(self, *args, **kwargs):
                self.a = 1
                self.b = 2
                self.c = 3

        obj = MyClass()
        self.assertEqual(obj.a, 1)
        self.assertEqual(obj.b, 2)
        self.assertEqual(obj.c, 3)
        self.assertFalse(hasattr(obj, b'__metaclass__'))
        self.assertIsInstance(obj, _ImmutableMixin)


class ImmutableMetaClassTests(TestCase):
    """Unit tests for beanbag_licensing.immutable.__ImmutableMetaClass."""

    def test_class_state(self):
        """Testing __ImmutableMetaClass class state"""
        self.assertFalse(hasattr(ImmutableMetaClass, b'__metaclass__'))
        self.assertEqual(ImmutableMetaClass.__bases__[0].__name__, b'__ImmutableAttrsMetaMetaClass')

    def test_delete_class_attr(self):
        """Testing __ImmutableMetaClass and deleting class attributes fails"""
        with self.assertRaises(AttributeError):
            del ImmutableMetaClass.__setattr__
        with self.assertRaises(AttributeError):
            delattr(ImmutableMetaClass, b'__setattr__')
        with self.assertRaises(AttributeError):
            del ImmutableMetaClass.new_var
        with self.assertRaises(TypeError):
            del ImmutableMetaClass.__dict__[b'__setattr__']

    def test_set_class_attr(self):
        """Testing __ImmutableMetaClass and setting class attributes fails"""
        with self.assertRaises(AttributeError):
            ImmutableMetaClass.__setattr__ = lambda *args: None
        with self.assertRaises(AttributeError):
            setattr(ImmutableMetaClass, b'__setattr__', lambda *args: None)
        with self.assertRaises(AttributeError):
            ImmutableMetaClass.new_var = lambda *args: None
        with self.assertRaises(TypeError):
            ImmutableMetaClass.__dict__[b'__setattr__'] = lambda *args: None


class ImmutableAttrsMetaClassTests(TestCase):
    """Unit tests for beanbag_licensing.immutable.__ImmutableAttrsMetaClass."""

    def test_class_state(self):
        """Testing __ImmutableAttrsMetaClass class state"""
        self.assertFalse(hasattr(ImmutableAttrsMetaClass, b'__metaclass__'))
        self.assertEqual(ImmutableAttrsMetaClass.__bases__, (type,))

    def test_delete_class_attr(self):
        """Testing __ImmutableAttrsMetaClass and deleting class attributes
        fails
        """
        with self.assertRaises(AttributeError):
            del ImmutableAttrsMetaClass.__setattr__
        with self.assertRaises(AttributeError):
            delattr(ImmutableAttrsMetaClass, b'__setattr__')
        with self.assertRaises(AttributeError):
            del ImmutableAttrsMetaClass.new_var
        with self.assertRaises(TypeError):
            del ImmutableAttrsMetaClass.__dict__[b'__setattr__']

    def test_set_class_attr(self):
        """Testing __ImmutableAttrsMetaClass and setting class attributes fails
        """
        with self.assertRaises(AttributeError):
            ImmutableAttrsMetaClass.__setattr__ = lambda *args: None
        with self.assertRaises(AttributeError):
            setattr(ImmutableAttrsMetaClass, b'__setattr__', lambda *args: None)
        with self.assertRaises(AttributeError):
            ImmutableAttrsMetaClass.new_var = lambda *args: None
        with self.assertRaises(TypeError):
            ImmutableAttrsMetaClass.__dict__[b'__setattr__'] = lambda *args: None


class ImmutableTests(TestCase):
    """Unit tests for beanbag_licensing.immutable.immutable."""

    def test_subclass_replace_immutable_init(self):
        """Testing @immutable-based class and replacing __init__ and
        __immutable_init__ fails
        """

        @immutable
        class MyClass(object):

            def __init__(self, *args, **kwargs):
                pass

        with self.assertRaises(AttributeError):
            MyClass.__init__ = lambda *args: None
        with self.assertRaises(AttributeError):
            MyClass.__immutable_init__ = lambda *args: None

    def test_subclass_set_immutable_attrs(self):
        """Testing @immutable-based class and setting immutable attrs"""

        @immutable
        class MyClass(object):
            immutable_attrs = ('a', )

            def __init__(self):
                self.a = 1

        obj = MyClass()
        with self.assertRaisesMessage(AttributeError, b'Cannot modify immutable attribute'):
            obj.a = 100
        self.assertEqual(obj.a, 1)

    def test_subclass_delete_immutable_attrs(self):
        """Testing @immutable-based class and deleting immutable attrs"""

        @immutable
        class MyClass(object):
            immutable_attrs = ('a', )

            def __init__(self):
                self.a = 1

        obj = MyClass()
        message = b'Cannot delete immutable attribute'
        with self.assertRaisesMessage(AttributeError, message):
            del obj.a
        with self.assertRaisesMessage(AttributeError, message):
            delattr(obj, b'a')
        with self.assertRaisesMessage(AttributeError, b"'MyClass' object has no attribute '__dict__'"):
            del obj.__dict__[b'a']
        self.assertEqual(obj.a, 1)

    def test_subclass_set_mutable_attrs(self):
        """Testing @immutable-based class and setting mutable attrs"""

        @immutable
        class MyClass(object):
            mutable_attrs = ('a', 'b')

        obj = MyClass()
        obj.a = 1
        obj.b = 2
        self.assertEqual(obj.a, 1)
        self.assertEqual(obj.b, 2)

    def test_subclass_delete_mutable_attrs(self):
        """Testing @immutable-based class and deleting mutable attrs"""

        @immutable
        class MyClass(object):
            mutable_attrs = ('a', )

            def __init__(self):
                self.a = 1

        obj = MyClass()
        del obj.a
        self.assertFalse(hasattr(obj, b'a'))