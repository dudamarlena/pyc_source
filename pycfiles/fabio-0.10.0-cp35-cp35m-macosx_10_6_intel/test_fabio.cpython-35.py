# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/test_fabio.py
# Compiled at: 2019-03-04 08:01:16
# Size of source mod 2**32: 2819 bytes
from __future__ import print_function, with_statement, division, absolute_import
import unittest, logging
logger = logging.getLogger(__name__)
from .utilstest import UtilsTest
import fabio

class TestFabio(unittest.TestCase):

    def test_open(self):
        filename = UtilsTest.getimage('multiframes.edf.bz2')
        filename = filename.replace('.bz2', '')
        image = fabio.open(filename)
        image.data
        image.close()

    def test_open_with(self):
        filename = UtilsTest.getimage('multiframes.edf.bz2')
        filename = filename.replace('.bz2', '')
        with fabio.open(filename) as (image):
            image.data

    def test_open_series(self):
        filename = UtilsTest.getimage('multiframes.edf.bz2')
        filename = filename.replace('.bz2', '')
        series = fabio.open_series(filenames=[filename])
        for _frame in series.frames():
            pass

        series.close()

    def test_open_series_with(self):
        filename = UtilsTest.getimage('multiframes.edf.bz2')
        filename = filename.replace('.bz2', '')
        with fabio.open_series(filenames=[filename]) as (series):
            for _frame in series.frames():
                pass

    def test_open_series_first_filename(self):
        filename = UtilsTest.getimage('multiframes.edf.bz2')
        filename = filename.replace('.bz2', '')
        with fabio.open_series(first_filename=filename) as (series):
            for _frame in series.frames():
                pass


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestFabio))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())