# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/joe/code/python/eximloganalyzer/src/eximloganalyzer/tests/tests_configfile.py
# Compiled at: 2010-07-18 04:41:54
import unittest
from eximloganalyzer.config import Config

class ConfigFileTests(unittest.TestCase):
    """Tests the general functionality of the config file"""

    def setUp(self):
        """Some initialization stuff"""
        self.configFile = 'tests/eximloganalyzer.cfg'

    def testOpenConfigPass(self):
        """Tests if Config object can open the config file"""
        self.failUnless(Config(self.configFile))

    def testOpenConfigFail(self):
        """Tests if Config raises if it can't open the config file"""
        self.assertRaises(IOError, Config, 'Idontexist.cfg')

    def testGetRulesPass(self):
        """Tests if Config can parse rules from ini file"""
        c = Config(self.configFile)
        rules = c.getRules()
        r = False
        for rule in rules:
            if rule[0] == 'Outgoing via Cron':
                r = True

        self.assertTrue(r)

    def testGetRulesFail(self):
        """Tests if Config fails when can't parse ini file"""
        badConfigFile = 'tests/badconfig.cfg'
        c = Config(badConfigFile)
        self.assertFalse(c.getRules())