# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ngen/tests/test_singletons.py
# Compiled at: 2017-10-08 17:55:08
from __future__ import absolute_import, print_function, unicode_literals
import unittest
from ngen.singletons import Singleton

class Catalog(Singleton):
    registry = {}

    def register(self, name, value):
        self.registry[name] = value


Catalog()

class Mixin(object):

    def inspect(self):
        return self.registry.keys()


class Greetings(Catalog, Mixin):
    pass


class Workers(Catalog):
    pass


class SingletonTests(unittest.TestCase):

    def setUp(self):
        Workers._instance = None
        Greetings._instance = None
        return

    def test_singleton_pattern(self):
        workers1 = Workers()
        workers2 = Workers()
        self.assertTrue(workers1 is workers2)

    def test_inheritance(self):
        workers = Workers()
        greetings = Greetings()
        self.assertFalse(workers is greetings)

    def test_registry_persists(self):
        workers = Workers()
        workers.register(b'foo', b'bar')
        self.assertEqual(workers.registry[b'foo'], b'bar')
        workers2 = Workers()
        self.assertEqual(workers2.registry[b'foo'], b'bar')
        greetings = Greetings()
        greetings.register(b'asdf', b'lkj')
        self.assertEqual(greetings.registry[b'asdf'], b'lkj')
        greetings2 = Greetings()
        self.assertEqual(greetings2.registry[b'asdf'], b'lkj')

    def test_repr(self):
        workers = Workers()
        self.assertIsInstance(repr(workers), str)


if __name__ == b'__main__':
    unittest.main()