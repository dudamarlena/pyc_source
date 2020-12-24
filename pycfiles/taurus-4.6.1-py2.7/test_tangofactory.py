# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/tango/test/test_tangofactory.py
# Compiled at: 2019-08-19 15:09:29
"""Tests for taurus.core.tango.tangofactory"""
import taurus
from taurus.external.unittest import TestCase
from taurus.core.tango.test.tgtestds import TangoSchemeTestLauncher

class TestFactoryGarbageCollection(TangoSchemeTestLauncher, TestCase):
    DEV_NAME = 'TangoSchemeTest/unittest/temp-tfgc-1'

    def setUp(self):
        self.factory = taurus.Factory()

    def test_device(self):
        old_len = len(self.factory.tango_devs)

        def create():
            taurus.Device(self.DEV_NAME)

        create()
        msg = 'factory is polluted with device'
        self.assertEqual(len(self.factory.tango_devs), old_len, msg)

    def test_attribute(self):
        old_len = len(self.factory.tango_attrs)

        def create():
            taurus.Attribute(self.DEV_NAME + '/state')

        create()
        msg = 'factory is polluted with attribute'
        self.assertEqual(len(self.factory.tango_attrs), old_len, msg)

    def tearDown(self):
        self.factory = None
        return