# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/codecs/test_edfimage1.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 19205 bytes
"""
# Unit tests
Reading edf files as originally specified by expg with fabio.module edfimage.py

07/06/2019 PB
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, os, numpy, shutil, io, logging
logger = logging.getLogger(__name__)
import fabio
from fabio.edfimage import edfimage
from ..utilstest import UtilsTest

def fopen(filename=None, frameno=None):
    header = None
    data = None
    frame = None
    logging.debug('fopen(filename={},frameno={})'.format(filename, frameno))
    if filename:
        image = fabio.open(filename)
        if frameno is None:
            frameno = 0
        nframes = image.nframes
        if hasattr(image, 'npsdframes'):
            npsdframes = image.npsdframes
            nerrorframes = image.nerrorframes
        else:
            npsdframes = nframes
            nerrorframes = 0
        if frameno >= npsdframes:
            logging.warning('Psd frame {} out of range: 0 <= {} < {}'.format(frameno, frameno, npsdframes))
        if frameno < 0:
            if -frameno > nerrorframes:
                logging.warning('Error frame {} out of range: {} <= {} < 0 '.format(frameno, -nerrorframes, frameno))
            frameno += nframes
        if frameno in range(nframes):
            if nframes > 1:
                frame = image.getframe(frameno)
                data = frame.data
                header = frame.header
            else:
                data = image.data
                header = image.header
            frame = fabio.fabioimage.FabioFrame(data=data, header=header)
    else:
        raise IOError('fopen: Cannot access frame: {} (0<=frame<{})'.format(frameno, nframes))
    return frame


def get_data_counts(shape=None):
    """
    Counts all items specified by shape
    """
    if shape is None:
        shape = ()
    counts = 1
    for ishape in range(0, len(shape)):
        counts *= shape[ishape]

    return counts


def test_00(cls, filename, avglist=None, keylist=None):
    """
    Checks the correct shape of the data arrays.
    Compares the mean value of each data frame array, with the number given in avglist.
    filename: name of file to test
    avglist: list of average values for each frame, stops, if not equal
    keylist: list of keys to read, stops, if not available
    If avglist or keylist is shorter than frameno, the last value in the list is used.
    """
    image = fabio.open(filename)
    nframes = image.nframes
    if hasattr(image, 'npsdframes'):
        npsdframes = image.npsdframes
        nerrorframes = image.nerrorframes
    else:
        npsdframes = image.nframes
        nerrorframes = 0
    for frameno in range(0, npsdframes):
        frame = fopen(filename, frameno)
        counts = get_data_counts(frame.shape)
        data_counts = get_data_counts(frame.data.shape)
        cls.assertEqual(counts, data_counts, 'A:filename={},frameno={}: inconsistent data shapes: header.{},data.{}'.format(filename, frameno, frame.shape, frame.data.shape))
        sum = numpy.sum(frame.data)
        fmean = sum / counts
        logging.debug('filename={},frameno={},sum={},counts={},fmean={}'.format(filename, frameno, sum, counts, fmean))
        if avglist is not None:
            if len(avglist) > frameno:
                avg = avglist[frameno]
            else:
                avg = avglist[(-1)]
            cls.assertLessEqual(abs(fmean - avg), abs(fmean + avg) * 5e-06, 'B:filename={},frameno={}: unexpected average value: calculated {}, expected {}'.format(filename, frameno, fmean, avg))
        if keylist is not None:
            if len(keylist) > frameno:
                key = keylist[frameno]
            else:
                key = keylist[(-1)]
            if key in frame.header:
                logging.debug("filename={}, frameno={}: '{}' = {}".format(filename, frameno, key, frame.header[key]))
            else:
                logging.debug("filename={}, frameno={}: '{}' = None".format(filename, frameno, key))
            cls.assertIn(key, frame.header, "C:filename={},frameno={}: Missing expected header key '{}'".format(filename, frameno, key))

    for frameno in range(0, nerrorframes):
        frame = fopen(filename, -frameno - 1)
        counts = get_data_counts(frame.shape)
        data_counts = get_data_counts(frame.data.shape)
        cls.assertEqual(counts, data_counts, 'D:filename={},frameno={}: inconsistent data shapes: header.{},data.{}'.format(filename, frameno, frame.shape, frame.data.shape))
        sum = numpy.sum(frame.data)
        fmean = sum / counts
        logging.debug('filename={},frameno={},sum={},counts={},fmean={}'.format(filename, frameno, sum, counts, fmean))
        if avglist is not None:
            if len(avglist) > nframes - frameno - 1:
                avg = avglist[(nframes - frameno - 1)]
            else:
                avg = avglist[(-1)]
            cls.assertLessEqual(abs(fmean - avg), abs(fmean + avg) * 5e-06, 'E:filename={},frameno={}: unexpected average value: calculated {}, expected {}'.format(filename, frameno, fmean, avg))
        if keylist is not None:
            if len(keylist) > nframes - frameno - 1:
                key = keylist[(nframes - frameno - 1)]
            else:
                key = keylist[(-1)]
            if key in frame.header:
                logging.debug("filename={},frameno={}: key='{}'".format(filename, frameno, key, frame.header[key]))
            else:
                logging.debug('filename={},frameno={}: key=None'.format(filename, frameno, key))
            cls.assertIn(key, frame.header, "F:filename={},frameno={}: Missing expected header key '{}'".format(filename, frameno, key))


class EdfBlockBoundaryCases(unittest.TestCase):
    __doc__ = '\n    Test some special cases\n    '

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.files = UtilsTest.resources.getdir('ehf_images2.tar.bz2')
        self.root = os.path.join(self.files[0], '..')

    def test_edfblocktypes(self):
        """
        Test reading (gzipped) extended edf multi frame data files with and without a general block
        The files have been prepared with make_multiedfs.sh.
        The pixel values of each frame are equal to the frame number for checking reading the correct data.
        multi5.edf.gz:      5 frames without general block, preset frameno
        multi5+gblk.edf.gz: 5 frames starting with general block, preset to frameno,
                            DefaultKey added to the general block, it must be available for all frames
        multi5_gzip.edf      : like multi5.edf.gz, but with internal compression
        multi5+gblk_gzip.edf : like multi5+gblk.edf.gz, but with internal compression
        """
        avglist = [
         0.0, 1.0, 2.0, 3.0, 4.0]
        filename = os.path.join(self.root, '00_edfblocktypes/multi5.edf.gz')
        test_00(self, filename, avglist)
        keylist = ['DefaultKey']
        filename = os.path.join(self.root, '00_edfblocktypes/multi5+gblk.edf.gz')
        test_00(self, filename, avglist, keylist)
        filename = os.path.join(self.root, '00_edfblocktypes/multi5+gblk_gzip.edf')
        test_00(self, filename, avglist)
        filename = os.path.join(self.root, '00_edfblocktypes/multi5_gzip.edf')
        test_00(self, filename, avglist)

    def test_edfsingle_raw_bf_gblk(self):
        """
        Reading an uncompressed edf-single-frame-file with references to data
        in externally saved dataframes.
        Check average data value, and verify that the key ExperimentInfo is
        correctly read from the general block.

        """
        avglist = [
         25743.2]
        filename = os.path.join(self.root, '01_single_raw_bf_gblk/pj19_frelon_00028_raw.ehf')
        keylist = ['ExperimentInfo']
        test_00(self, filename, avglist, keylist)

    def test_edfmulti_raw_bf_gblk(self):
        """
        Reading an uncompressed edf-multi-frame-file with references to data
        in externally saved dataframes and checking the average of each frame.
        Some header values are modified for checking the robustness.
        frames 0..16: Test reading from a multi frame edf file with links to
                      external binary files (ehf)
        frame 17:     Test reading without EDF_BinaryFileSize => must be
                      estimated from data size
        frame 18:     Test reading with EDF_BinaryFileSize bigger than required
                      => currently an unnecessary info is given
        """
        avglist = [
         9584.23, 9592.64, 9591.69, 9599.7, 9602.51, 9604.29, 9610.97, 9609.86, 9614.14, 9610.52, 9603.12, 9603.27, 9600.22, 9606.86, 9605.26, 9601.37, 9606.09, 9604.51, 9604.45, 9617.5]
        filename = os.path.join(self.root, '02_multi_raw_bf_gblk/rh28a_saxs_00022_raw_binned.ehf')
        test_00(self, filename, avglist)

    def test_edfmulti_raw_dark_raw_bf_gblk(self):
        """
        Linking data of several frames to different parts of a single external
        binary file.
        rh28a_saxs_00003_dark_binned.ehf:
          WARNING:fabio.edfimage:Under-short header frame 2: only 311 bytes
             => this should disappear when reading EDF_BlockBoundary
          INFO:fabio.edfimage:Data stream is padded : 29184 > required 28800 bytes
            => unnecessary, it cannot be avoided, e.g. for saving byte arrays of odd length
        rh28a_saxs_00003_raw_binned.ehf:
          INFO:fabio.edfimage:Data stream is padded : 29184 > required 28800 bytes
            => unnecessary, feature, e.g. for saving byte arrays of odd length
        """
        avglist = [
         2487.36, 2488.28, 2488.11]
        filename = os.path.join(self.root, '03_multi_raw_dark_bf_gblk/rh28a_saxs_00003_dark_binned.ehf')
        test_00(self, filename, avglist)
        avglist = [9651.25]
        filename = os.path.join(self.root, '03_multi_raw_dark_bf_gblk/rh28a_saxs_00003_raw_binned.ehf')
        test_00(self, filename, avglist)

    def test_edfsingle_raw_bf_gblk_gz(self):
        """
        Test reading gzipped data files linking to an external binary data file.
        Check that the extension .gz is added to the name of the external binary
        data file if it cannot be opened with the binary file name found in the
        header. Both files are gzipped.
        """
        avglist = [
         25743.2]
        filename = os.path.join(self.root, '04_single_raw_bf_gblk_gz/pj19_frelon_00028_raw.ehf.gz')
        test_00(self, filename, avglist)

    def test_edfsingle_raw_bf_gblk_gz(self):
        """
        Test reading gzipped data files linking to an external binary data file.
        Check that the extension .gz is added to the name of the external binary
        data file if it cannot be opened with the binary file name found in the
        header. The binary data file is not compressed.
        """
        avglist = [
         25743.2]
        filename = os.path.join(self.root, '05_single_raw_bf_gblk_gz/pj19_frelon_00028_raw.ehf.gz')
        test_00(self, filename, avglist)

    def test_edf6_single_raw_bf_gblk_gz(self):
        """
        Test reading gzipped data files linking to an external binary data file.
        Check that the extension .gz is added to the name of the external binary
        data file if it cannot be opened with the binary file name found in the
        header. Only the binary data file is gzipped.
        """
        avglist = [
         25743.2]
        filename = os.path.join(self.root, '06_single_raw_bf_gblk_gz/pj19_frelon_00028_raw.ehf')
        test_00(self, filename, avglist)

    def test_edfmulti_raw_bf_gblk_gz(self):
        """
        Test reading the files of the test test_edfmulti_raw_bf_gblk after
        gzipping.
        Test reading from multi frame files, like test_edfmulti_raw_bf_gblk, but
        but with all files gzipped.
        frames 0..16: Test reading from a multi frame edf file with links to
                      external binary files (ehf)
        frame 17:     Test reading without EDF_BinaryFileSize => should be
                      estimated from data size
        frame 18:     Test reading with EDF_BinaryFileSize bigger than required
                      => currently an unnecessary info is given
        frame 19:     Test reading with a wrong EDF_BinaryFileSize that excceeds
                      the real file size. => data must only be read to the end
                      of the binary data file.
        """
        avglist = [
         9584.23, 9592.64, 9591.69, 9599.7, 9602.51, 9604.29, 9610.97, 9609.86, 9614.14, 9610.52, 9603.12, 9603.27, 9600.22, 9606.86, 9605.26, 9601.37, 9606.09, 9604.51, 9604.45, 9617.5]
        filename = os.path.join(self.root, '07_multi_raw_bf_gblk_gz/rh28a_saxs_00022_raw_binned.ehf.gz')
        test_00(self, filename, avglist)

    def test_pitfalls(self):
        """
        multi5+headerblob_edf1.edf.gz
        multi5+headerblob+headerendinheader_edf1.edf.gz
        multi5+pitfalls_edf1.edf.gz
        multi5+headerblob_edf0.edf.gz
        multi5+headerblob+headerendinheader_edf0.edf.gz
        multi5+pitfalls_edf0.edf.gz
        """
        avglist = [
         0, 1, 2, 3, 4]
        filename = os.path.join(self.root, '08_pitfalls/multi5+pitfalls_edf1.edf.gz')
        test_00(self, filename, avglist)
        avglist = [
         18312, 18312, 18312, 18312, 18312]
        filename = os.path.join(self.root, '08_pitfalls/multi5+headerblob_edf1.edf.gz')
        test_00(self, filename, avglist)
        filename = os.path.join(self.root, '08_pitfalls/multi5+headerblob+headerendinheader_edf1.edf.gz')
        test_00(self, filename, avglist)
        avglist = [
         0, 1, 2, 3, 4]
        filename = os.path.join(self.root, '08_pitfalls/multi5+pitfalls_edf0.edf.gz')
        test_00(self, filename, avglist)
        avglist = [
         18312, 18312, 18312, 18312, 18312]
        filename = os.path.join(self.root, '08_pitfalls/multi5+headerblob_edf0.edf.gz')
        test_00(self, filename, avglist)

    def test_special(self):
        """
        09_special/face_ok.edf.gz
        09_special/face_headerendatboundary1.edf.gz
        09_special/face_headerendatboundary2.edf.gz
        09_special/face_headerendatboundary3.edf.gz
        09_special/face_tooshort.edf.gz
        """
        avglist = [
         0.178897]
        filename = os.path.join(self.root, '09_special/face_ok.edf.gz')
        test_00(self, filename, avglist)
        avglist = [
         0.178897]
        filename = os.path.join(self.root, '09_special/face_headerendatboundary1.edf.gz')
        test_00(self, filename, avglist)
        filename = os.path.join(self.root, '09_special/face_headerendatboundary2.edf.gz')
        test_00(self, filename, avglist)
        filename = os.path.join(self.root, '09_special/face_headerendatboundary3.edf.gz')
        test_00(self, filename, avglist)


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(EdfBlockBoundaryCases))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())