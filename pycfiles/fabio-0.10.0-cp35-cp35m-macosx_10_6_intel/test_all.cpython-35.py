# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/test_all.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 2797 bytes
"""Test suite for all fabio modules."""
from __future__ import print_function, with_statement, division, absolute_import
import sys, logging, unittest
logger = logging.getLogger(__name__)
from . import testfabioimage
from . import testfilenames
from . import test_file_series
from . import test_filename_steps
from . import testheadernotsingleton
from . import testopenheader
from . import testopenimage
from . import test_flat_binary
from . import testcompression
from . import test_nexus
from . import testfabioconvert
from . import test_failing_files
from . import test_formats
from . import test_image_convert
from . import test_tiffio
from . import test_frames
from . import test_fabio
from . import codecs
from . import test_agi_bitfield

def suite():
    testSuite = unittest.TestSuite()
    testSuite.addTest(testfabioimage.suite())
    testSuite.addTest(testfilenames.suite())
    testSuite.addTest(test_file_series.suite())
    testSuite.addTest(test_filename_steps.suite())
    testSuite.addTest(testheadernotsingleton.suite())
    testSuite.addTest(testopenheader.suite())
    testSuite.addTest(testopenimage.suite())
    testSuite.addTest(test_flat_binary.suite())
    testSuite.addTest(testcompression.suite())
    testSuite.addTest(test_nexus.suite())
    testSuite.addTest(testfabioconvert.suite())
    testSuite.addTest(test_failing_files.suite())
    testSuite.addTest(test_formats.suite())
    testSuite.addTest(test_image_convert.suite())
    testSuite.addTest(test_tiffio.suite())
    testSuite.addTest(test_frames.suite())
    testSuite.addTest(test_fabio.suite())
    testSuite.addTest(codecs.suite())
    testSuite.addTest(test_agi_bitfield.suite())
    return testSuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    if not runner.run(suite()).wasSuccessful():
        sys.exit(1)