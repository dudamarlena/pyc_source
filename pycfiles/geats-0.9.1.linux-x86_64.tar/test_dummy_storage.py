# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/geats/tests/test_dummy_storage.py
# Compiled at: 2012-05-10 07:35:56
import unittest
from ..storage.dummystoragevolume import DummyStorageVolume

class DummyStorageTest(unittest.TestCase):

    def setUp(self):
        self.volume = DummyStorageVolume('vda', {'name': 'vda', 
           'blockdevice': '/dev/DOES_NOT_EXIST'}, vm=None, config={})
        return

    def test_get_name(self):
        self.assertEqual(self.volume.get_name(), 'vda')

    def test_activate_volume(self):
        self.volume.activate()

    def test_deactivate_volume(self):
        self.volume.deactivate()

    def test_format_volume(self):
        self.volume.format()

    def test_get_blockdevice(self):
        self.assertEqual('/dev/DOES_NOT_EXIST', self.volume.get_blockdevice())

    def test_is_local(self):
        self.assertTrue(self.volume.is_local())