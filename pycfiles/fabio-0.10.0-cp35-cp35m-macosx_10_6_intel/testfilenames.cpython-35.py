# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/testfilenames.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 4333 bytes
"""
Test cases for filename deconstruction

testsuite by Jerome Kieffer (Jerome.Kieffer@esrf.eu)
28/11/2014
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, os, logging
logger = logging.getLogger(__name__)
import fabio
CASES = [
 (1, 'edf', 'data0001.edf'),
 (10001, 'edf', 'data10001.edf'),
 (10001, 'edf', 'data10001.edf.gz'),
 (10001, 'edf', 'data10001.edf.bz2'),
 (2, 'marccd', 'data0002.mccd'),
 (12345, 'marccd', 'data12345.mccd'),
 (10001, 'marccd', 'data10001.mccd.gz'),
 (10001, 'marccd', 'data10001.mccd.bz2'),
 (123, 'marccd', 'data123.mccd.gz'),
 (3, 'tif_or_pilatus', 'data0003.tif'),
 (4, 'tif_or_pilatus', 'data0004.tiff'),
 (12, 'bruker', 'sucrose101.012.gz'),
 (99, 'bruker', 'sucrose101.099'),
 (99, 'bruker', 'sucrose101.0099'),
 (99, 'bruker', 'sucrose101.0099.bz2'),
 (99, 'bruker', 'sucrose101.0099.gz'),
 (2, 'fit2dmask', 'fit2d.msk'),
 (None, 'fit2dmask', 'mymask.msk'),
 (670005, 'edf', 'S82P670005.edf'),
 (670005, 'edf', 'S82P670005.edf.gz'),
 (1, 'dtrek_or_oxd_or_hipic_or_raxis', 'mb_LP_1_001.img'),
 (2, 'dtrek_or_oxd_or_hipic_or_raxis', 'mb_LP_1_002.img.gz'),
 (3, 'dtrek_or_oxd_or_hipic_or_raxis', 'mb_LP_1_003.img.bz2'),
 (
  3, 'dtrek_or_oxd_or_hipic_or_raxis', os.path.join('data', 'mb_LP_1_003.img.bz2'))]
MORE_CASES = [
 ('data0010.edf', 'data0012.edf', 10),
 ('data1000.pnm', 'data999.pnm', 1000),
 ('data0999.pnm', 'data1000.pnm', 999),
 ('data123457.edf', 'data123456.edf', 123457),
 ('d0ata000100.mccd', 'd0ata000012.mccd', 100),
 (
  os.path.join('images/sampledir', 'P33S670003.edf'),
  os.path.join('images/sampledir', 'P33S670002.edf'), 670003),
 (
  os.path.join('images/P33S67', 'P33S670003.edf'),
  os.path.join('images/P33S67', 'P33S670002.edf'), 670003),
 ('image2301.mar2300', 'image2300.mar2300', 2301),
 ('image2300.mar2300', 'image2301.mar2300', 2300),
 ('image.0123', 'image.1234', 123),
 ('mymask.msk', 'mymask.msk', None),
 ('data_123.mccd.bz2', 'data_001.mccd.bz2', 123)]

class TestFilenames(unittest.TestCase):
    __doc__ = ' check the name -> number, type conversions '

    def test_many_cases(self):
        """ loop over CASES """
        for num, typ, name in CASES:
            obj = fabio.FilenameObject(filename=name)
            self.assertEqual(num, obj.num, name + ' num=' + str(num) + ' != obj.num=' + str(obj.num))
            self.assertEqual(typ, '_or_'.join(obj.format), name + ' ' + '_or_'.join(obj.format))
            self.assertEqual(name, obj.tostring(), name + ' ' + obj.tostring())

    def test_more_cases(self):
        for nname, oname, num in MORE_CASES:
            name = fabio.construct_filename(oname, num)
            self.assertEqual(name, nname)

    def test_more_cases_jump(self):
        for nname, oname, num in MORE_CASES:
            name = fabio.jump_filename(oname, num)
            self.assertEqual(name, nname)


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestFilenames))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())