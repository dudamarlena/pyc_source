# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/codecs/test_dtrekimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 7667 bytes
"""
Unit tests for the d*TREK format.
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, os, logging, numpy, shutil
from ..utilstest import UtilsTest
logger = logging.getLogger(__name__)
import fabio
from fabio.dtrekimage import DtrekImage
from fabio.edfimage import EdfImage
from fabio.utils import testutils
TESTIMAGES = [
 (
  'mb_LP_1_001.img', (3072, 3072), 0.0, 65535.0, 120.33, 147.38,
  {'BEAM_CENTER_Y': '157.500000'}),
 (
  'mb_LP_1_001.img.gz', (3072, 3072), 0.0, 65535.0, 120.33, 147.38,
  {'BEAM_CENTER_Y': '157.500000'}),
 (
  'mb_LP_1_001.img.bz2', (3072, 3072), 0.0, 65535.0, 120.33, 147.38,
  {'BEAM_CENTER_Y': '157.500000'}),
 (
  'HSA_1_5mg_C1_0004.img', (385, 775), -2, 2127, 69.25, 59.52,
  {'WAVELENGTH': '1.0 1.541870'})]

class TestMatch(unittest.TestCase):
    __doc__ = '\n    check the ??fit2d?? conversion to edf gives same numbers\n    '

    def setUp(self):
        """ Download images """
        self.fn_adsc = UtilsTest.getimage('mb_LP_1_001.img.bz2')[:-4]
        self.fn_edf = UtilsTest.getimage('mb_LP_1_001.edf.bz2')[:-4]

    def testsame(self):
        """test ADSC image match to EDF"""
        im1 = EdfImage()
        im1.read(self.fn_edf)
        im2 = DtrekImage()
        im2.read(self.fn_adsc)
        diff = im1.data.astype('float32') - im2.data.astype('float32')
        logger.debug('type: %s %s shape %s %s ' % (im1.data.dtype, im2.data.dtype, im1.data.shape, im2.data.shape))
        logger.debug('im1 min %s %s max %s %s ' % (im1.data.min(), im2.data.min(), im1.data.max(), im2.data.max()))
        logger.debug('delta min %s max %s mean %s' % (diff.min(), diff.max(), diff.mean()))
        self.assertEqual(abs(diff).max(), 0.0, 'asdc data == edf data')


class TestDtrekImplementation(testutils.ParametricTestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmp_directory = os.path.join(UtilsTest.tempdir, cls.__name__)
        os.makedirs(cls.tmp_directory)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp_directory)

    def setUp(self):
        unittest.TestCase.setUp(self)

    def test_write_and_read_cube(self):
        input_type = numpy.uint16
        data = numpy.arange(100).reshape(5, 10, 2)
        data = data.astype(input_type)
        obj = DtrekImage(data=data)
        filename = os.path.join(self.tmp_directory, 'cube.img')
        obj.save(filename)
        self.assertEqual(obj.data.dtype.type, input_type)
        obj2 = fabio.open(filename)
        self.assertEqual(obj2.data.dtype.type, input_type)
        self.assertEqual(obj.shape, obj2.shape)
        numpy.testing.assert_array_almost_equal(obj.data, obj2.data)

    def test_write_and_read_empty(self):
        obj = DtrekImage(data=None)
        filename = os.path.join(self.tmp_directory, 'cube.img')
        obj.save(filename)
        obj2 = fabio.open(filename)
        self.assertEqual(obj2.data, None)
        self.assertEqual(obj.data, obj2.data)

    def test_write_and_read(self):
        configs = [
         (
          numpy.uint16, 'little_endian', None),
         (
          numpy.uint16, 'big_endian', None),
         (
          numpy.uint32, 'little_endian', None),
         (
          numpy.int32, 'little_endian', None),
         (
          numpy.float32, 'little_endian', None),
         (
          numpy.float32, 'little_endian', None),
         (
          numpy.uint64, 'little_endian', numpy.uint32),
         (
          numpy.int64, 'little_endian', numpy.int32),
         (
          numpy.float16, 'little_endian', numpy.float32)]
        for config in configs:
            with self.subTest(config=config):
                input_type, byte_order, output_type = config
                if output_type is None:
                    output_type = input_type
                header = {}
                header['BYTE_ORDER'] = byte_order
                data = numpy.arange(50).reshape(5, 10)
                data = data.astype(input_type)
                obj = DtrekImage(data=data, header=header)
                filename = os.path.join(self.tmp_directory, 'saved_%s.img' % hash(config))
                obj.save(filename)
                self.assertEqual(obj.data.dtype.type, input_type)
                obj2 = fabio.open(filename)
                self.assertEqual(obj2.data.dtype.type, output_type)
                self.assertEqual(obj.shape, obj2.shape)
                if input_type == output_type:
                    numpy.testing.assert_array_almost_equal(obj.data, obj2.data)


class TestRealSamples(testutils.ParametricTestCase):
    __doc__ = '\n    Test real samples stored in our archive.\n    '

    @classmethod
    def setUpClass(cls):
        """Prefetch images"""
        download = []
        for datainfo in TESTIMAGES:
            name = datainfo[0]
            if name.endswith('.bz2'):
                download.append(name)
            else:
                if name.endswith('.gz'):
                    download.append(name[:-3] + '.bz2')
                else:
                    download.append(name + '.bz2')

        download = list(set(download))
        for name in download:
            os.path.dirname(UtilsTest.getimage(name))

        cls.im_dir = UtilsTest.resources.data_home

    def test_read(self):
        """ check we can read flat ADSC images"""
        for datainfo in TESTIMAGES:
            with self.subTest(datainfo=datainfo):
                name, shape, mini, maxi, mean, stddev, keys = datainfo
                obj = DtrekImage()
                obj.read(os.path.join(self.im_dir, name))
                self.assertAlmostEqual(mini, obj.getmin(), 2, 'getmin')
                self.assertAlmostEqual(maxi, obj.getmax(), 2, 'getmax')
                got_mean = obj.getmean()
                self.assertAlmostEqual(mean, got_mean, 2, 'getmean exp %s != got %s' % (mean, got_mean))
                self.assertAlmostEqual(stddev, obj.getstddev(), 2, 'getstddev')
                for key, value in keys.items():
                    self.assertIn(key, obj.header)
                    self.assertEqual(value, obj.header[key])

                self.assertEqual(shape, obj.shape)


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestMatch))
    testsuite.addTest(loadTests(TestRealSamples))
    testsuite.addTest(loadTests(TestDtrekImplementation))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())