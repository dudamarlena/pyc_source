# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/test_formats.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 3146 bytes
"""
# Unit tests

# builds on stuff from ImageD11.test.testpeaksearch
28/11/2014
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, logging
logger = logging.getLogger(__name__)
import fabio
from .. import fabioformats
from ..utils import deprecation
from ..utils import testutils

class TestRegistration(unittest.TestCase):

    def test_fabio_factory(self):
        image = fabio.factory('edfimage')
        self.assertIsNotNone(image)

    def test_fabio_factory_missing_format(self):
        self.assertRaises(RuntimeError, fabio.factory, 'foobarimage')

    def test_fabioformats_factory(self):
        image = fabioformats.factory('edfimage')
        self.assertIsNotNone(image)

    def test_fabioformats_factory_missing_format(self):
        self.assertRaises(RuntimeError, fabioformats.factory, 'foobarimage')

    @testutils.test_logging(deprecation.depreclog, warning=1)
    def test_deprecated_fabioimage_factory(self):
        """Check that it is still working"""
        image = fabio.fabioimage.FabioImage.factory('edfimage')
        self.assertIsNotNone(image)

    @testutils.test_logging(deprecation.depreclog, warning=1)
    def test_deprecated_fabioimage_factory_missing_format(self):
        """Check that it is still working"""
        self.assertRaises(RuntimeError, fabio.fabioimage.FabioImage.factory, 'foobarimage')

    def test_not_existing(self):
        self.assertIsNone(fabioformats.get_class_by_name('myformat0'))

    def test_annotation(self):

        @fabio.register
        class MyFormat1(fabio.fabioimage.FabioImage):
            pass

        self.assertIsNotNone(fabioformats.get_class_by_name('myformat1'))

    def test_function(self):

        class MyFormat2(fabio.fabioimage.FabioImage):
            pass

        fabio.register(MyFormat2)
        self.assertIsNotNone(fabioformats.get_class_by_name('myformat2'))


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestRegistration))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())