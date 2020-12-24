# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jmcfarlane/dev/Chula/tests/unit/test_system.py
# Compiled at: 2011-03-19 21:05:04
import unittest
from chula import system

class Test_system(unittest.TestCase):
    doctest = system

    def setUp(self):
        self.system = system.System()

    def test_os_type_was_able_to_be_determined(self):
        self.failIf(self.system.type == 'UNKNOWN')

    def test_number_of_processors_able_to_be_determined(self):
        self.failIf(self.system.procs <= 0)