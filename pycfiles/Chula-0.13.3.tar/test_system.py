# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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