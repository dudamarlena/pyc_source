# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/joekavalieri/git/redisengine/tests/trees/test_proxy_queryset.py
# Compiled at: 2016-04-05 18:00:40
import unittest
from time import time
from redisengine import fields, exceptions
from redisengine.proxy.tree import ProxyTree
from redisengine.connection import connect, get_connection, register_connection
__all__ = ('TestProxyTreeQueryset', )

class TestProxyTreeQueryset(unittest.TestCase):

    def setUp(self):
        connect(10)
        self.db = get_connection()

        class Person(ProxyTree):
            name = fields.StringField()
            age = fields.IntField()

        class ComplexPerson(ProxyTree):
            name = fields.StringField()
            age = fields.IntField()
            addressess = fields.ListField()

        self.Person = Person
        self.ComplexPerson = ComplexPerson

    def tearDown(self):
        self.db.flushdb()

    def test_all(self):
        person = self.ComplexPerson(name='Joe', age=234, addressess=['234'])
        person.save()
        all_persons = self.ComplexPerson.proxy_tree.all()
        self.assertEqual(list(all_persons)[0], person)