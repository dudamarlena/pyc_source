# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\test\test_sequence.py
# Compiled at: 2017-01-26 21:08:30
# Size of source mod 2**32: 2280 bytes
"""unittest cases for Sequence class"""
import unittest
from dicom.dataset import Dataset
from dicom.sequence import Sequence

class SequenceTests(unittest.TestCase):

    def testDefaultInitialization(self):
        """Sequence: Ensure a valid Sequence is created"""
        empty = Sequence()
        self.assertTrue(len(empty) == 0, 'Non-empty Sequence created')

    def testValidInitialization(self):
        """Sequence: Ensure valid creation of Sequences using Dataset inputs"""
        inputs = {'PatientPosition': 'HFS', 
         'PatientSetupNumber': '1', 
         'SetupTechniqueDescription': ''}
        patientSetups = Dataset()
        patientSetups.update(inputs)
        seq = Sequence((patientSetups,))
        self.assertTrue(isinstance(seq[0], Dataset), 'Dataset modified during Sequence creation')

    def testInvalidInitialization(self):
        """Sequence: Raise error if inputs are not iterables or Datasets"""
        self.assertRaises(TypeError, Sequence, Dataset())
        self.assertRaises(TypeError, Sequence, 1)
        self.assertRaises(TypeError, Sequence, [1, 2])

    def testInvalidAssignment(self):
        """Sequence: validate exception for invalid assignment"""
        seq = Sequence([Dataset()])
        self.assertRaises(TypeError, seq.__setitem__, 0, 1)

    def testValidAssignment(self):
        """Sequence: ensure ability to assign a Dataset to a Sequence item"""
        ds = Dataset()
        ds.add_new((1, 1), 'IS', 1)
        seq = Sequence([Dataset()])
        seq[0] = ds
        self.assertEqual(seq[0], ds, 'Dataset modified during assignment')


if __name__ == '__main__':
    unittest.main()