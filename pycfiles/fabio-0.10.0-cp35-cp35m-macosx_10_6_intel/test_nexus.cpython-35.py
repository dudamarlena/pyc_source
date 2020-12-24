# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/test_nexus.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 2621 bytes
"""Unit tests for nexus file reader
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, os, logging
logger = logging.getLogger(__name__)
from .utilstest import UtilsTest
from .. import nexus

class TestNexus(unittest.TestCase):

    def setUp(self):
        if nexus.h5py is None:
            self.skipTest('h5py library is not available. Skipping Nexus test')

    def test_nexus(self):
        """Test creation of Nexus files"""
        fname = os.path.join(UtilsTest.tempdir, 'nexus.h5')
        nex = nexus.Nexus(fname)
        entry = nex.new_entry('entry')
        nex.new_instrument(entry, 'ID00')
        nex.new_detector('camera')
        self.assertEqual(len(nex.get_entries()), 2, 'nexus file has 2 entries')
        nex.close()
        self.assertTrue(os.path.exists(fname))
        os.unlink(fname)

    def test_from_time(self):
        fname = os.path.join(UtilsTest.tempdir, 'nexus.h5')
        nex = nexus.Nexus(fname)
        entry = nex.new_entry('entry')
        time1 = nexus.from_isotime(entry['start_time'][()])
        entry['bad_time'] = [entry['start_time'][()]]
        time2 = nexus.from_isotime(entry['bad_time'][()])
        self.assertEqual(time1, time2, 'start_time in list does not works !')
        nex.close()
        self.assertTrue(os.path.exists(fname))
        os.unlink(fname)


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestNexus))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())