# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hikaruhorie/workspace/hikaruhorie/django_enum/django_enum/tests.py
# Compiled at: 2016-03-28 13:00:16
from __future__ import division, print_function, absolute_import
from . import enum
from django.core.exceptions import ImproperlyConfigured
from django.db import models
import os, unittest

class TestEnum(unittest.TestCase):

    def setUp(self):

        class MyEnum(enum.Enum):
            __order__ = 'FOO BAR FOOBAR'
            FOO = ('f', 'Foo')
            BAR = ('b', 'Bar')
            FOOBAR = ('fb', 'FooBar')

        self.enum_class = MyEnum
        self.max_length = 2
        self.tuples = [
         ('f', 'Foo'),
         ('b', 'Bar'),
         ('fb', 'FooBar')]

    def test_get_by_key(self):
        self.assertEqual(self.enum_class.get_by_key('f'), self.enum_class.FOO)
        self.assertEqual(self.enum_class.get_by_key('b'), self.enum_class.BAR)
        self.assertEqual(self.enum_class.get_by_key('fb'), self.enum_class.FOOBAR)

    def test_tuples(self):
        self.assertEqual(self.enum_class.tuples(), self.tuples)

    def test_choices(self):
        self.assertEqual(self.enum_class.choices(), self.tuples)

    def test_get_max_length(self, **kwargs):
        self.assertEqual(self.enum_class.get_max_length(), self.max_length)


class TestEnumField(unittest.TestCase):

    def setUp(self):

        class MyEnum(enum.Enum):
            __order__ = 'FOO BAR FOOBAR'
            FOO = ('f', 'Foo')
            BAR = ('b', 'Bar')
            FOOBAR = ('fb', 'FooBar')

        class MyModel(models.Model):
            enum = enum.EnumField(enum=MyEnum, default=MyEnum.BAR)

        self.enum_class = MyEnum
        self.model_class = MyModel
        self.max_length = 2
        self.tuples = [
         ('f', 'Foo'),
         ('b', 'Bar'),
         ('fb', 'FooBar')]

    def test___init__(self):
        self.assertEqual(self.enum_class, self.model_class.enum)


if __name__ == '__main__':
    unittest.main()