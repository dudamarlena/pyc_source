# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_seatbelt/tests.py
# Compiled at: 2011-07-06 12:18:00
import sys
from testtools import TestCase
from django_seatbelt import seatbelt

class SeatbeltTests(TestCase):

    def test_fasten_restores_sys_path(self):
        orig_path = sys.path[:]
        with seatbelt.fasten():
            pass
        final_path = sys.path[:]
        self.assertEqual(orig_path, final_path)

    def test_fasten_filters_out_stuff(self):
        sys.path.append('foo')
        self.assertIn('foo', sys.path)
        with seatbelt.fasten([lambda path: path != 'foo']):
            self.assertNotIn('foo', sys.path)
        self.assertIn('foo', sys.path)

    def test_fasten_gets_rid_of_usr_local_by_default(self):
        sys.path.append('/usr/local/SEATBELT')
        with seatbelt.fasten([lambda path: path.__eq__('foo')]):
            self.assertNotIn('/usr/local/SEATBELT', sys.path)

    def test_solder_filters_stuff_forever(self):
        sys.path.append('foo')
        self.assertIn('foo', sys.path)
        seatbelt.solder([lambda path: path != 'foo'])
        self.assertNotIn('foo', sys.path)