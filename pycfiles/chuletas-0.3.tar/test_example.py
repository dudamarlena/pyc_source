# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jmcfarlane/dev/Chula/tests/unit/test_example.py
# Compiled at: 2011-03-19 21:05:04
import unittest
from chula import example

class Test_example(unittest.TestCase):
    doctest = example

    def setUp(self):
        self.something = 'This gets reset at the start of every test'
        self.db = 'Sometimes you will set a db and cursor here'
        self.example = example.Example()

    def tearDown(self):
        self.something = 'This resets it after each test'

    def test_something(self):
        self.assertEquals([], example.something())

    def test_sum(self):
        self.assertEquals(3, self.example.sum(1, 2))
        self.assertRaises(TypeError, self.example.sum, (1, '2'))

    def test_awesome(self):
        self.failIf(not self.example.awesome())