# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\test\test_dictionary.py
# Compiled at: 2017-01-26 21:08:30
# Size of source mod 2**32: 1997 bytes
"""Test suite for dicom_dictionary.py"""
import unittest
from dicom.tag import Tag
from dicom.datadict import CleanName, all_names_for_tag, dictionary_description

class DictTests(unittest.TestCase):

    def testCleanName(self):
        """dicom_dictionary: CleanName returns correct strings............."""
        self.assertTrue(CleanName(1048592) == 'PatientsName')
        self.assertTrue(CleanName(Tag((16, 16))) == 'PatientsName')

    def testTagNotFound(self):
        """dicom_dictionary: CleanName returns blank string for unknown tag"""
        self.assertTrue(CleanName(2576945425) == '')

    def testNameFinding(self):
        """dicom_dictionary: get long and short names for a data_element name"""
        names = all_names_for_tag(Tag(805961906))
        expected = ['TreatmentMachineName']
        self.assertEqual(names, expected, 'Expected %s, got %s' % (expected, names))
        names = all_names_for_tag(Tag(805962016))
        expected = ['BeamLimitingDeviceAngle', 'BLDAngle']
        self.assertEqual(names, expected, 'Expected %s, got %s' % (expected, names))

    def testRepeaters(self):
        """dicom_dictionary: Tags with "x" return correct dict info........"""
        self.assertEqual(dictionary_description(2622464), 'Transform Label')
        self.assertEqual(dictionary_description(2622480), 'Rows For Nth Order Coefficients')


class PrivateDictTests(unittest.TestCase):

    def testPrivate1(self):
        """private dict: """
        self.assertTrue(CleanName(1048592) == 'PatientsName')
        self.assertTrue(CleanName(Tag((16, 16))) == 'PatientsName')


if __name__ == '__main__':
    unittest.main()