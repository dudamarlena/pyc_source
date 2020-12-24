# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\test\test_charset.py
# Compiled at: 2017-01-26 21:10:17
# Size of source mod 2**32: 2933 bytes
"""unittest cases for dicom.charset module"""
import unittest, dicom, os.path
from pkg_resources import Requirement, resource_filename
testcharset_dir = resource_filename(Requirement.parse('dicom'), 'dicom/testcharsetfiles')
latin1_file = os.path.join(testcharset_dir, 'chrFren.dcm')
jp_file = os.path.join(testcharset_dir, 'chrH31.dcm')
multiPN_file = os.path.join(testcharset_dir, 'chrFrenMulti.dcm')
sq_encoding_file = os.path.join(testcharset_dir, 'chrSQEncoding.dcm')
test_dir = resource_filename(Requirement.parse('dicom'), 'dicom/testfiles')
normal_file = os.path.join(test_dir, 'CT_small.dcm')

class charsetTests(unittest.TestCase):

    def testLatin1(self):
        """charset: can read and decode latin_1 file........................"""
        ds = dicom.read_file(latin1_file)
        ds.decode()
        expected = 'Buc^Jérôme'
        got = ds.PatientName
        self.assertEqual(expected, got, 'Expected %r, got %r' % (expected, got))

    def testNestedCharacterSets(self):
        """charset: can read and decode SQ with different encodings........."""
        ds = dicom.read_file(sq_encoding_file)
        ds.decode()
        expected = 'ﾔﾏﾀﾞ^ﾀﾛｳ=山田^太郎=やまだ^たろう'
        got = ds[(50, 4196)][0].PatientName
        self.assertEqual(expected, got, 'Expected %r, got %r' % (expected, got))

    def testStandardFile(self):
        """charset: can read and decode standard file without special char.."""
        ds = dicom.read_file(normal_file)
        ds.decode()

    def testMultiPN(self):
        """charset: can decode file with multi-valued data elements........."""
        ds = dicom.read_file(multiPN_file)
        ds.decode()


if __name__ == '__main__':
    import sys, os, os.path
    dir_name = os.path.dirname(sys.argv[0])
    save_dir = os.getcwd()
    if dir_name:
        os.chdir(dir_name)
    os.chdir('../testfiles')
    unittest.main()
    os.chdir(save_dir)