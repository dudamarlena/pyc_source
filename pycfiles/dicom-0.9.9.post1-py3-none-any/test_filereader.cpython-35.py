# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\test\test_filereader.py
# Compiled at: 2017-01-26 21:10:18
# Size of source mod 2**32: 20969 bytes
"""unittest tests for dicom.filereader module"""
import sys, os, os.path, unittest
from io import BytesIO
import shutil
stat_available = True
try:
    from os import stat
except:
    stat_available = False

have_numpy = True
try:
    import numpy
except:
    have_numpy = False

from dicom.filereader import read_file
from dicom.errors import InvalidDicomError
from dicom.tag import Tag, TupleTag
import dicom.valuerep, gzip
from dicom.test.warncheck import assertWarns
from pkg_resources import Requirement, resource_filename
test_dir = resource_filename(Requirement.parse('dicom'), 'dicom/testfiles')
rtplan_name = os.path.join(test_dir, 'rtplan.dcm')
rtdose_name = os.path.join(test_dir, 'rtdose.dcm')
ct_name = os.path.join(test_dir, 'CT_small.dcm')
mr_name = os.path.join(test_dir, 'MR_small.dcm')
jpeg2000_name = os.path.join(test_dir, 'JPEG2000.dcm')
jpeg_lossy_name = os.path.join(test_dir, 'JPEG-lossy.dcm')
jpeg_lossless_name = os.path.join(test_dir, 'JPEG-LL.dcm')
deflate_name = os.path.join(test_dir, 'image_dfl.dcm')
rtstruct_name = os.path.join(test_dir, 'rtstruct.dcm')
priv_SQ_name = os.path.join(test_dir, 'priv_SQ.dcm')
nested_priv_SQ_name = os.path.join(test_dir, 'nested_priv_SQ.dcm')
no_meta_group_length = os.path.join(test_dir, 'no_meta_group_length.dcm')
gzip_name = os.path.join(test_dir, 'zipMR.gz')
dir_name = os.path.dirname(sys.argv[0])
save_dir = os.getcwd()

def isClose(a, b, epsilon=1e-06):
    """Compare within some tolerance, to avoid machine roundoff differences"""
    try:
        a.append
    except:
        return abs(a - b) < epsilon
    else:
        if len(a) != len(b):
            return False
        else:
            for ai, bi in zip(a, b):
                if abs(ai - bi) > epsilon:
                    return False

            return True


class ReaderTests(unittest.TestCase):

    def testRTPlan(self):
        """Returns correct values for sample data elements in test RT Plan file"""
        plan = read_file(rtplan_name)
        beam = plan.BeamSequence[0]
        cp0, cp1 = beam.ControlPointSequence
        self.assertEqual(beam.TreatmentMachineName, 'unit001', 'Incorrect unit name')
        self.assertEqual(beam.TreatmentMachineName, beam[(12298, 178)].value, 'beam TreatmentMachineName does not match the value accessed by tag number')
        got = cp1.ReferencedDoseReferenceSequence[0].CumulativeDoseReferenceCoefficient
        DS = dicom.valuerep.DS
        expected = DS('0.9990268')
        self.assertTrue(got == expected, "Cum Dose Ref Coeff not the expected value (CP1, Ref'd Dose Ref")
        got = cp0.BeamLimitingDevicePositionSequence[0].LeafJawPositions
        self.assertTrue(got[0] == DS('-100') and got[1] == DS('100.0'), 'X jaws not as expected (control point 0)')

    def testRTDose(self):
        """Returns correct values for sample data elements in test RT Dose file"""
        dose = read_file(rtdose_name)
        self.assertEqual(dose.FrameIncrementPointer, Tag((12292, 12)), 'Frame Increment Pointer not the expected value')
        self.assertEqual(dose.FrameIncrementPointer, dose[(40, 9)].value, 'FrameIncrementPointer does not match the value accessed by tag number')
        fract = dose.ReferencedRTPlanSequence[0].ReferencedFractionGroupSequence[0]
        beamnum = fract.ReferencedBeamSequence[0].ReferencedBeamNumber
        self.assertEqual(beamnum, 1, 'Beam number not the expected value')

    def testCT(self):
        """Returns correct values for sample data elements in test CT file...."""
        ct = read_file(ct_name)
        self.assertEqual(ct.file_meta.ImplementationClassUID, '1.3.6.1.4.1.5962.2', 'ImplementationClassUID not the expected value')
        self.assertEqual(ct.file_meta.ImplementationClassUID, ct.file_meta[(2, 18)].value, 'ImplementationClassUID does not match the value accessed by tag number')
        got = ct.ImagePositionPatient
        DS = dicom.valuerep.DS
        expected = [DS('-158.135803'), DS('-179.035797'), DS('-75.699997')]
        self.assertTrue(got == expected, 'ImagePosition(Patient) values not as expected.got {0}, expected {1}'.format(got, expected))
        self.assertEqual(ct.Rows, 128, 'Rows not 128')
        self.assertEqual(ct.Columns, 128, 'Columns not 128')
        self.assertEqual(ct.BitsStored, 16, 'Bits Stored not 16')
        self.assertEqual(len(ct.PixelData), 32768, 'Pixel data not expected length')
        expected = '[Duration of X-ray on]'
        got = ct[(67, 4174)].name
        msg = "Mismatch in private tag name, expected '%s', got '%s'"
        self.assertEqual(expected, got, msg % (expected, got))
        if have_numpy:
            expected = 909
            got = ct.pixel_array[(-1)][(-1)]
            msg = 'Did not get correct value for last pixel: expected %d, got %r' % (expected, got)
            self.assertEqual(expected, got, msg)
        else:
            print('**Numpy not available -- pixel array test skipped**')

    def testNoForce(self):
        """Raises exception if missing DICOM header and force==False..........."""
        self.assertRaises(InvalidDicomError, read_file, rtstruct_name)

    def testRTstruct(self):
        """Returns correct values for sample elements in test RTSTRUCT file...."""
        rtss = read_file(rtstruct_name, force=True)
        expected = '1.2.840.10008.1.2'
        got = rtss.file_meta.TransferSyntaxUID
        msg = 'Expected transfer syntax %r, got %r' % (expected, got)
        self.assertEqual(expected, got, msg)
        frame_of_ref = rtss.ReferencedFrameOfReferenceSequence[0]
        study = frame_of_ref.RTReferencedStudySequence[0]
        uid = study.RTReferencedSeriesSequence[0].SeriesInstanceUID
        expected = '1.2.826.0.1.3680043.8.498.2010020400001.2.1.1'
        msg = "Expected Reference Series UID '%s', got '%s'" % (expected, uid)
        self.assertEqual(expected, uid, msg)
        got = rtss.ROIContourSequence[0].ContourSequence[2].ContourNumber
        expected = 3
        msg = 'Expected Contour Number %d, got %r' % (expected, got)
        self.assertEqual(expected, got, msg)
        obs_seq0 = rtss.RTROIObservationsSequence[0]
        got = obs_seq0.ROIPhysicalPropertiesSequence[0].ROIPhysicalProperty
        expected = 'REL_ELEC_DENSITY'
        msg = "Expected Physical Property '%s', got %r" % (expected, got)
        self.assertEqual(expected, got, msg)

    def testDir(self):
        """Returns correct dir attributes for both Dataset and DICOM names (python >= 2.6).."""
        rtss = read_file(rtstruct_name, force=True)
        got_dir = dir(rtss)
        expect_in_dir = ['pixel_array', 'add_new', 'ROIContourSequence',
         'StructureSetDate', '__sizeof__']
        expect_not_in_dir = ['RemovePrivateTags', 'AddNew', 'GroupDataset']
        for name in expect_in_dir:
            self.assertTrue(name in got_dir, "Expected name '%s' in dir()" % name)

        for name in expect_not_in_dir:
            self.assertTrue(name not in got_dir, "Unexpected name '%s' in dir()" % name)

        roi0 = rtss.ROIContourSequence[0]
        got_dir = dir(roi0)
        expect_in_dir = ['pixel_array', 'add_new', 'ReferencedROINumber',
         'ROIDisplayColor', '__sizeof__']
        for name in expect_in_dir:
            self.assertTrue(name in got_dir, "Expected name '%s' in dir()" % name)

    def testMR(self):
        """Returns correct values for sample data elements in test MR file....."""
        mr = read_file(mr_name)
        mr.decode()
        self.assertEqual(mr.PatientName, 'CompressedSamples^MR1', 'Wrong patient name')
        self.assertEqual(mr.PatientName, mr[(16, 16)].value, 'Name does not match value found when accessed by tag number')
        got = mr.PixelSpacing
        DS = dicom.valuerep.DS
        expected = [DS('0.3125'), DS('0.3125')]
        self.assertTrue(got == expected, 'Wrong pixel spacing')

    def testDeflate(self):
        """Returns correct values for sample data elements in test compressed (zlib deflate) file"""
        ds = read_file(deflate_name)
        got = ds.ConversionType
        expected = 'WSD'
        self.assertEqual(got, expected, "Attempted to read deflated file data element Conversion Type, expected '%s', got '%s'" % (expected, got))

    def testNoPixelsRead(self):
        """Returns all data elements before pixels using stop_before_pixels=False"""
        ctpartial = read_file(ct_name, stop_before_pixels=True)
        ctpartial_tags = sorted(ctpartial.keys())
        ctfull = read_file(ct_name)
        ctfull_tags = sorted(ctfull.keys())
        msg = 'Tag list of partial CT read (except pixel tag and padding) did not match full read'
        msg += '\nExpected: %r\nGot %r' % (ctfull_tags[:-2], ctpartial_tags)
        missing = [Tag(32736, 16), Tag(65532, 65532)]
        self.assertEqual(ctfull_tags, ctpartial_tags + missing, msg)

    def testPrivateSQ(self):
        """Can read private undefined length SQ without error...................."""
        read_file(priv_SQ_name)

    def testNestedPrivateSQ(self):
        """Can successfully read a private SQ which contains additional SQ's....."""
        ds = read_file(nested_priv_SQ_name)
        pixel_data_tag = TupleTag((32736, 16))
        self.assertTrue(pixel_data_tag in ds, 'Entire dataset was not parsed properly. PixelData is not present')
        tag = TupleTag((1, 1))
        seq0 = ds[tag]
        self.assertEqual(seq0.VR, 'SQ', 'First level sequence not parsed properly')
        seq1 = seq0[0][tag]
        self.assertEqual(seq1.VR, 'SQ', 'Second level sequence not parsed properly')
        got = seq1[0][tag].value
        expected = b'Double Nested SQ'
        self.assertEqual(got, expected, "Expected a value of %s, got %s'" % (expected, got))
        got = seq0[0][(1, 2)].value
        expected = b'Nested SQ'
        self.assertEqual(got, expected, "Expected a value of %s, got %s'" % (expected, got))

    def testNoMetaGroupLength(self):
        """Read file with no group length in file meta..........................."""
        ds = read_file(no_meta_group_length)
        got = ds.InstanceCreationDate
        expected = '20111130'
        self.assertEqual(got, expected, "Sample data element after file meta with no group length failed, expected '%s', got '%s'" % (expected, got))


class JPEG2000Tests(unittest.TestCase):

    def setUp(self):
        self.jpeg = read_file(jpeg2000_name)

    def testJPEG2000(self):
        """JPEG2000: Returns correct values for sample data elements............"""
        expected = [
         Tag(84, 16), Tag(84, 32)]
        got = self.jpeg.FrameIncrementPointer
        self.assertEqual(got, expected, 'JPEG2000 file, Frame Increment Pointer: expected %s, got %s' % (expected, got))
        got = self.jpeg.DerivationCodeSequence[0].CodeMeaning
        expected = 'Lossy Compression'
        self.assertEqual(got, expected, 'JPEG200 file, Code Meaning got %s, expected %s' % (got, expected))

    def testJPEG2000PixelArray(self):
        """JPEG2000: Fails gracefully when uncompressed data is asked for......."""
        self.assertRaises(NotImplementedError, self.jpeg._get_pixel_array)


class JPEGlossyTests(unittest.TestCase):

    def setUp(self):
        self.jpeg = read_file(jpeg_lossy_name)

    def testJPEGlossy(self):
        """JPEG-lossy: Returns correct values for sample data elements.........."""
        got = self.jpeg.DerivationCodeSequence[0].CodeMeaning
        expected = 'Lossy Compression'
        self.assertEqual(got, expected, 'JPEG-lossy file, Code Meaning got %s, expected %s' % (got, expected))

    def testJPEGlossyPixelArray(self):
        """JPEG-lossy: Fails gracefully when uncompressed data is asked for....."""
        self.assertRaises(NotImplementedError, self.jpeg._get_pixel_array)


class JPEGlosslessTests(unittest.TestCase):

    def setUp(self):
        self.jpeg = read_file(jpeg_lossless_name)

    def testJPEGlossless(self):
        """JPEGlossless: Returns correct values for sample data elements........"""
        got = self.jpeg.SourceImageSequence[0].PurposeOfReferenceCodeSequence[0].CodeMeaning
        expected = 'Uncompressed predecessor'
        self.assertEqual(got, expected, 'JPEG-lossless file, Code Meaning got %s, expected %s' % (got, expected))

    def testJPEGlosslessPixelArray(self):
        """JPEGlossless: Fails gracefully when uncompressed data is asked for..."""
        self.assertRaises(NotImplementedError, self.jpeg._get_pixel_array)


class DeferredReadTests(unittest.TestCase):
    __doc__ = 'Test that deferred data element reading (for large size)\n    works as expected\n    '

    def setUp(self):
        self.testfile_name = ct_name + '.tmp'
        shutil.copyfile(ct_name, self.testfile_name)

    def testTimeCheck(self):
        """Deferred read warns if file has been modified..........."""
        if stat_available:
            ds = read_file(self.testfile_name, defer_size=2000)
            from time import sleep
            sleep(1)
            with open(self.testfile_name, 'r+') as (f):
                f.write('\x00')
            warning_start = 'Deferred read warning -- file modification time '

            def read_value():
                ds.PixelData

            assertWarns(self, warning_start, read_value)

    def testFileExists(self):
        """Deferred read raises error if file no longer exists....."""
        ds = read_file(self.testfile_name, defer_size=2000)
        os.remove(self.testfile_name)

        def read_value():
            ds.PixelData

        self.assertRaises(IOError, read_value)

    def testValuesIdentical(self):
        """Deferred values exactly matches normal read..............."""
        ds_norm = read_file(self.testfile_name)
        ds_defer = read_file(self.testfile_name, defer_size=2000)
        for data_elem in ds_norm:
            tag = data_elem.tag
            self.assertEqual(data_elem.value, ds_defer[tag].value, 'Mismatched value for tag %r' % tag)

    def testZippedDeferred(self):
        """Deferred values from a gzipped file works.............."""
        fobj = gzip.open(gzip_name)
        ds = read_file(fobj, defer_size=1)
        fobj.close()
        ds.InstanceNumber

    def tearDown(self):
        if os.path.exists(self.testfile_name):
            os.remove(self.testfile_name)


class FileLikeTests(unittest.TestCase):
    __doc__ = 'Test that can read DICOM files with file-like object rather than filename'

    def testReadFileGivenFileObject(self):
        """filereader: can read using already opened file............"""
        f = open(ct_name, 'rb')
        ct = read_file(f)
        got = ct.ImagePositionPatient
        DS = dicom.valuerep.DS
        expected = [DS('-158.135803'), DS('-179.035797'), DS('-75.699997')]
        self.assertTrue(got == expected, 'ImagePosition(Patient) values not as expected')
        self.assertEqual(ct.file_meta.ImplementationClassUID, '1.3.6.1.4.1.5962.2', 'ImplementationClassUID not the expected value')
        self.assertEqual(ct.file_meta.ImplementationClassUID, ct.file_meta[(2, 18)].value, 'ImplementationClassUID does not match the value accessed by tag number')
        got = ct.ImagePositionPatient
        expected = [DS('-158.135803'), DS('-179.035797'), DS('-75.699997')]
        self.assertTrue(got == expected, 'ImagePosition(Patient) values not as expected')
        self.assertEqual(ct.Rows, 128, 'Rows not 128')
        self.assertEqual(ct.Columns, 128, 'Columns not 128')
        self.assertEqual(ct.BitsStored, 16, 'Bits Stored not 16')
        self.assertEqual(len(ct.PixelData), 32768, 'Pixel data not expected length')
        f.close()

    def testReadFileGivenFileLikeObject(self):
        """filereader: can read using a file-like (BytesIO) file...."""
        with open(ct_name, 'rb') as (f):
            file_like = BytesIO(f.read())
        ct = read_file(file_like)
        got = ct.ImagePositionPatient
        DS = dicom.valuerep.DS
        expected = [DS('-158.135803'), DS('-179.035797'), DS('-75.699997')]
        self.assertTrue(got == expected, 'ImagePosition(Patient) values not as expected')
        self.assertEqual(len(ct.PixelData), 32768, 'Pixel data not expected length')
        file_like.close()


if __name__ == '__main__':
    dir_name = os.path.dirname(sys.argv[0])
    save_dir = os.getcwd()
    if dir_name:
        os.chdir(dir_name)
    os.chdir('../testfiles')
    unittest.main()
    os.chdir(save_dir)