# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/test_flat_binary.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 2795 bytes
"""
Test cases for the flat binary images

testsuite by Jerome Kieffer (Jerome.Kieffer@esrf.eu)
28/11/2014
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, os, logging
from .utilstest import UtilsTest
logger = logging.getLogger(__name__)
import fabio

class TestFlatBinary(unittest.TestCase):
    filenames = [os.path.join(UtilsTest.tempdir, i) for i in ('not.a.file', 'bad_news_1234',
                                                              'empty_files_suck_1234.edf',
                                                              'notRUBY_1234.dat')]

    def setUp(self):
        for filename in self.filenames:
            with open(filename, 'wb') as (f):
                f.write('\x00x0' * 2048 * 2048 * 2)

    def test_openimage(self):
        """
        test the opening of "junk" empty images ...
        JK: I wonder if this test makes sense !
        """
        nfail = 0
        for filename in self.filenames:
            try:
                im = fabio.open(filename)
                if im.data.tobytes() != '\x00x0' * 2048 * 2048 * 2:
                    nfail += 1
                else:
                    logger.info('**** Passed: %s' % filename)
            except Exception:
                logger.warning('failed for: %s' % filename)
                nfail += 1

        self.assertEqual(nfail, 0, ' %s failures out of %s' % (nfail, len(self.filenames)))

    def tearDown(self):
        for filename in self.filenames:
            os.remove(filename)


def suite():
    testsuite = unittest.TestSuite()
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())