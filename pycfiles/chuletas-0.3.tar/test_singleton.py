# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jmcfarlane/dev/Chula/tests/unit/test_singleton.py
# Compiled at: 2011-03-19 21:05:04
import unittest
from chula import singleton

class Test_singleton(unittest.TestCase):
    doctest = singleton