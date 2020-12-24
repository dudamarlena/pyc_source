# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\test\test_filewriter.py
# Compiled at: 2017-01-26 21:08:30
# Size of source mod 2**32: 8447 bytes
"""unittest cases for dicom.filewriter module"""
import sys, os.path, os, unittest
from dicom.filereader import read_file
from dicom.filewriter import write_data_element
from dicom.dataset import Dataset, FileDataset
from dicom.sequence import Sequence
from dicom.util.hexutil import hex2bytes, bytes2hex
from dicom.filebase import DicomBytesIO
from dicom.dataelem import DataElement
from pkg_resources import Requirement, resource_filename
test_dir = resource_filename(Requirement.parse('dicom'), 'dicom/testfiles')
testcharset_dir = resource_filename(Requirement.parse('dicom'), 'dicom/testcharsetfiles')
rtplan_name = os.path.join(test_dir, 'rtplan.dcm')
rtdose_name = os.path.join(test_dir, 'rtdose.dcm')
ct_name = os.path.join(test_dir, 'CT_small.dcm')
mr_name = os.path.join(test_dir, 'MR_small.dcm')
jpeg_name = os.path.join(test_dir, 'JPEG2000.dcm')
unicode_name = os.path.join(testcharset_dir, 'chrH31.dcm')
multiPN_name = os.path.join(testcharset_dir, 'chrFrenMulti.dcm')
rtplan_out = rtplan_name + '2'
rtdose_out = rtdose_name + '2'
ct_out = ct_name + '2'
mr_out = mr_name + '2'
jpeg_out = jpeg_name + '2'
unicode_out = unicode_name + '2'
multiPN_out = multiPN_name + '2'

def files_identical(a, b):
    """Return a tuple (file a == file b, index of first difference)"""
    with open(a, 'rb') as (A):
        with open(b, 'rb') as (B):
            a_bytes = A.read()
            b_bytes = B.read()
    return bytes_identical(a_bytes, b_bytes)


def bytes_identical(a_bytes, b_bytes):
    """Return a tuple (bytes a == bytes b, index of first difference)"""
    if a_bytes == b_bytes:
        return (True, 0)
    else:
        pos = 0
        while a_bytes[pos] == b_bytes[pos]:
            pos += 1

        return (
         False, pos)


class WriteFileTests(unittest.TestCase):

    def compare(self, in_filename, out_filename, decode=False):
        """Read file1, write file2, then compare.
        Return value as for files_identical.
        """
        dataset = read_file(in_filename)
        if decode:
            dataset.decode()
        dataset.save_as(out_filename)
        same, pos = files_identical(in_filename, out_filename)
        self.assertTrue(same, 'Files are not identical - first difference at 0x%x' % pos)
        if os.path.exists(out_filename):
            os.remove(out_filename)

    def testRTPlan(self):
        """Input file, write back and verify them identical (RT Plan file)"""
        self.compare(rtplan_name, rtplan_out)

    def testRTDose(self):
        """Input file, write back and verify them identical (RT Dose file)"""
        self.compare(rtdose_name, rtdose_out)

    def testCT(self):
        """Input file, write back and verify them identical (CT file)....."""
        self.compare(ct_name, ct_out)

    def testMR(self):
        """Input file, write back and verify them identical (MR file)....."""
        self.compare(mr_name, mr_out)

    def testUnicode(self):
        """Ensure decoded string DataElements are written to file properly"""
        self.compare(unicode_name, unicode_out, decode=True)

    def testMultiPN(self):
        """Ensure multiple Person Names are written to the file correctly."""
        self.compare(multiPN_name, multiPN_out, decode=True)

    def testJPEG2000(self):
        """Input file, write back and verify them identical (JPEG2K file)."""
        self.compare(jpeg_name, jpeg_out)

    def testListItemWriteBack(self):
        """Change item in a list and confirm it is written to file      .."""
        DS_expected = 0
        CS_expected = 'new'
        SS_expected = 999
        ds = read_file(ct_name)
        ds.ImagePositionPatient[2] = DS_expected
        ds.ImageType[1] = CS_expected
        ds[(67, 4114)].value[0] = SS_expected
        ds.save_as(ct_out)
        ds = read_file(ct_out)
        self.assertTrue(ds.ImageType[1] == CS_expected, 'Item in a list not written correctly to file (VR=CS)')
        self.assertTrue(ds[4395026].value[0] == SS_expected, 'Item in a list not written correctly to file (VR=SS)')
        self.assertTrue(ds.ImagePositionPatient[2] == DS_expected, 'Item in a list not written correctly to file (VR=DS)')
        if os.path.exists(ct_out):
            os.remove(ct_out)


class WriteDataElementTests(unittest.TestCase):
    __doc__ = 'Attempt to write data elements has the expected behaviour'

    def setUp(self):
        self.f1 = DicomBytesIO()
        self.f1.is_little_endian = True
        self.f1.is_implicit_VR = True

    def test_empty_AT(self):
        """Write empty AT correctly.........."""
        data_elem = DataElement(2621449, 'AT', [])
        expected = hex2bytes(' 28 00 09 00 00 00 00 00')
        write_data_element(self.f1, data_elem)
        got = self.f1.parent.getvalue()
        msg = 'Did not write zero-length AT value correctly. Expected %r, got %r' % (
         bytes2hex(expected), bytes2hex(got))
        msg = '%r %r' % (type(expected), type(got))
        msg = "'%r' '%r'" % (expected, got)
        self.assertEqual(expected, got, msg)


class ScratchWriteTests(unittest.TestCase):
    __doc__ = 'Simple dataset from scratch, written in all endian/VR combinations'

    def setUp(self):
        ds = Dataset()
        ds.PatientName = 'Name^Patient'
        subitem1 = Dataset()
        subitem1.ContourNumber = 1
        subitem1.ContourData = ['2', '4', '8', '16']
        subitem2 = Dataset()
        subitem2.ContourNumber = 2
        subitem2.ContourData = ['32', '64', '128', '196']
        sub_ds = Dataset()
        sub_ds.ContourSequence = Sequence((subitem1, subitem2))
        ds.ROIContourSequence = Sequence((sub_ds,))
        self.ds = ds

    def compare_write(self, hex_std, file_ds):
        """Write file and compare with expected byte string

        :arg hex_std: the bytes which should be written, as space separated hex
        :arg file_ds: a FileDataset instance containing the dataset to write
        """
        out_filename = 'scratch.dcm'
        file_ds.save_as(out_filename)
        std = hex2bytes(hex_std)
        with open(out_filename, 'rb') as (f):
            bytes_written = f.read()
        same, pos = bytes_identical(std, bytes_written)
        self.assertTrue(same, 'Writing from scratch unexpected result - 1st diff at 0x%x' % pos)
        if os.path.exists(out_filename):
            os.remove(out_filename)

    def testImpl_LE_deflen_write(self):
        """Scratch Write for implicit VR little endian, defined length SQ's"""
        from dicom.test._write_stds import impl_LE_deflen_std_hex as std
        file_ds = FileDataset('test', self.ds)
        self.compare_write(std, file_ds)


if __name__ == '__main__':
    dir_name = os.path.dirname(sys.argv[0])
    save_dir = os.getcwd()
    if dir_name:
        os.chdir(dir_name)
    os.chdir('../testfiles')
    unittest.main()
    os.chdir(save_dir)