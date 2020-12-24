# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\test\test_dataset.py
# Compiled at: 2017-01-26 21:10:18
# Size of source mod 2**32: 13653 bytes
"""unittest cases for dicom.dataset module"""
import unittest
from dicom.dataset import Dataset, PropertyError
from dicom.dataelem import DataElement, RawDataElement
from dicom.tag import Tag
from dicom.sequence import Sequence
from dicom import in_py3

class DatasetTests(unittest.TestCase):

    def failUnlessRaises(self, excClass, callableObj, *args, **kwargs):
        """Redefine unittest Exception test to return the exception object"""
        try:
            callableObj(*args, **kwargs)
        except excClass as excObj:
            return excObj
        else:
            if hasattr(excClass, '__name__'):
                excName = excClass.__name__
            else:
                excName = str(excClass)
            raise self.failureException('{0:s} not raised'.format(excName))

    def failUnlessExceptionArgs(self, start_args, excClass, callableObj):
        """Check the expected args were returned from an exception
        start_args -- a string with the start of the expected message
        """
        if in_py3:
            with self.assertRaises(excClass) as (cm):
                callableObj()
            excObj = cm.exception
        else:
            excObj = self.assertRaises(excClass, callableObj)
        msg = '\nExpected Exception message:\n' + start_args
        msg += '\nGot:\n' + excObj.args[0]
        self.assertTrue(excObj.args[0].startswith(start_args), msg)

    def testAttributeErrorInProperty(self):
        """Dataset: AttributeError in property raises actual error message.."""
        ds = Dataset()
        ds.file_meta = Dataset()
        ds.PixelData = 'xyzlmnop'

        def callable_pixel_array():
            ds.pixel_array

        attribute_error_msg = 'AttributeError in pixel_array property: ' + "Dataset does not have attribute 'TransferSyntaxUID'"
        self.failUnlessExceptionArgs(attribute_error_msg, PropertyError, callable_pixel_array)

    def testTagExceptionPrint(self):
        ds = Dataset()
        ds.PatientID = '123456'
        ds.SmallestImagePixelValue = 0
        expected_msg = "Invalid tag (0028, 0106): object of type 'int' has no len()"
        self.failUnlessExceptionArgs(expected_msg, TypeError, lambda : str(ds))

    def testTagExceptionWalk(self):
        ds = Dataset()
        ds.PatientID = '123456'
        ds.SmallestImagePixelValue = 0
        expected_msg = "Invalid tag (0028, 0106): object of type 'int' has no len()"
        callback = lambda dataset, data_element: str(data_element)
        func = lambda : ds.walk(callback)
        self.failUnlessExceptionArgs(expected_msg, TypeError, func)

    def dummy_dataset(self):
        ds = Dataset()
        ds.add_new((12298, 178), 'SH', 'unit001')
        return ds

    def testSetNewDataElementByName(self):
        """Dataset: set new data_element by name............................"""
        ds = Dataset()
        ds.TreatmentMachineName = 'unit #1'
        data_element = ds[(12298, 178)]
        self.assertEqual(data_element.value, 'unit #1', 'Unable to set data_element by name')
        self.assertEqual(data_element.VR, 'SH', 'data_element not the expected VR')

    def testSetExistingDataElementByName(self):
        """Dataset: set existing data_element by name......................."""
        ds = self.dummy_dataset()
        ds.TreatmentMachineName = 'unit999'
        self.assertEqual(ds[(12298, 178)].value, 'unit999')

    def testSetNonDicom(self):
        """Dataset: can set class instance property (non-dicom)............."""
        ds = Dataset()
        ds.SomeVariableName = 42
        has_it = hasattr(ds, 'SomeVariableName')
        self.assertTrue(has_it, 'Variable did not get created')
        if has_it:
            self.assertEqual(ds.SomeVariableName, 42, 'There, but wrong value')

    def testMembership(self):
        """Dataset: can test if item present by 'if <name> in dataset'......"""
        ds = self.dummy_dataset()
        self.assertTrue('TreatmentMachineName' in ds, 'membership test failed')
        self.assertTrue('Dummyname' not in ds, 'non-member tested as member')

    def testContains(self):
        """Dataset: can test if item present by 'if <tag> in dataset'......."""
        ds = self.dummy_dataset()
        self.assertTrue((12298, 178) in ds, 'membership test failed')
        self.assertTrue([12298, 178] in ds, 'membership test failed when list used')
        self.assertTrue(805961906 in ds, 'membership test failed')
        self.assertTrue((16, 95) not in ds, 'non-member tested as member')

    def testGetExists1(self):
        """Dataset: dataset.get() returns an existing item by name.........."""
        ds = self.dummy_dataset()
        unit = ds.get('TreatmentMachineName', None)
        self.assertEqual(unit, 'unit001', 'dataset.get() did not return existing member by name')

    def testGetExists2(self):
        """Dataset: dataset.get() returns an existing item by long tag......"""
        ds = self.dummy_dataset()
        unit = ds.get(805961906, None).value
        self.assertEqual(unit, 'unit001', 'dataset.get() did not return existing member by long tag')

    def testGetExists3(self):
        """Dataset: dataset.get() returns an existing item by tuple tag....."""
        ds = self.dummy_dataset()
        unit = ds.get((12298, 178), None).value
        self.assertEqual(unit, 'unit001', 'dataset.get() did not return existing member by tuple tag')

    def testGetExists4(self):
        """Dataset: dataset.get() returns an existing item by Tag..........."""
        ds = self.dummy_dataset()
        unit = ds.get(Tag(805961906), None).value
        self.assertEqual(unit, 'unit001', 'dataset.get() did not return existing member by tuple tag')

    def testGetDefault1(self):
        """Dataset: dataset.get() returns default for non-existing name ...."""
        ds = self.dummy_dataset()
        not_there = ds.get('NotAMember', 'not-there')
        msg = 'dataset.get() did not return default value for non-member by name'
        self.assertEqual(not_there, 'not-there', msg)

    def testGetDefault2(self):
        """Dataset: dataset.get() returns default for non-existing tuple tag"""
        ds = self.dummy_dataset()
        not_there = ds.get((39321, 39321), 'not-there')
        msg = 'dataset.get() did not return default value for non-member by tuple tag'
        self.assertEqual(not_there, 'not-there', msg)

    def testGetDefault3(self):
        """Dataset: dataset.get() returns default for non-existing long tag."""
        ds = self.dummy_dataset()
        not_there = ds.get(2576980377, 'not-there')
        msg = 'dataset.get() did not return default value for non-member by long tag'
        self.assertEqual(not_there, 'not-there', msg)

    def testGetDefault4(self):
        """Dataset: dataset.get() returns default for non-existing Tag......"""
        ds = self.dummy_dataset()
        not_there = ds.get(Tag(2576980377), 'not-there')
        msg = 'dataset.get() did not return default value for non-member by Tag'
        self.assertEqual(not_there, 'not-there', msg)

    def testGetFromRaw(self):
        """Dataset: get(tag) returns same object as ds[tag] for raw element."""
        test_tag = 1048592
        test_elem = RawDataElement(Tag(test_tag), 'PN', 4, b'test', 0, True, True)
        ds = Dataset({Tag(test_tag): test_elem})
        by_get = ds.get(test_tag)
        by_item = ds[test_tag]
        msg = 'Dataset.get() returned different objects for ds.get(tag) and ds[tag]:\nBy get():%r\nBy ds[tag]:%r\n'
        self.assertEqual(by_get, by_item, msg % (by_get, by_item))

    def test__setitem__(self):
        """Dataset: if set an item, it must be a DataElement instance......."""

        def callSet():
            ds[(12298, 178)] = 'unit1'

        ds = Dataset()
        self.assertRaises(TypeError, callSet)

    def test_matching_tags(self):
        """Dataset: key and data_element.tag mismatch raises ValueError....."""

        def set_wrong_tag():
            ds[(16, 16)] = data_element

        ds = Dataset()
        data_element = DataElement((12298, 178), 'SH', 'unit001')
        self.assertRaises(ValueError, set_wrong_tag)

    def test_NamedMemberUpdated(self):
        """Dataset: if set data_element by tag, name also reflects change..."""
        ds = self.dummy_dataset()
        ds[(12298, 178)].value = 'moon_unit'
        self.assertEqual(ds.TreatmentMachineName, 'moon_unit', 'Member not updated')

    def testUpdate(self):
        """Dataset: update() method works with tag or name.................."""
        ds = self.dummy_dataset()
        pat_data_element = DataElement((16, 18), 'PN', 'Johnny')
        ds.update({'PatientName': 'John', (16, 18): pat_data_element})
        self.assertEqual(ds[(16, 16)].value, 'John', 'named data_element not set')
        self.assertEqual(ds[(16, 18)].value, 'Johnny', 'set by tag failed')

    def testDir(self):
        """Dataset: dir() returns sorted list of named data_elements........"""
        ds = self.dummy_dataset()
        ds.PatientName = 'name'
        ds.PatientID = 'id'
        ds.NonDicomVariable = 'junk'
        ds.add_new((24, 4433), 'IS', 150)
        ds.add_new((4369, 291), 'DS', '42.0')
        expected = ['PatientID', 'PatientName', 'TreatmentMachineName',
         'XRayTubeCurrent']
        self.assertEqual(ds.dir(), expected, 'dir() returned %s, expected %s' % (str(ds.dir()), str(expected)))

    def testDeleteDicomAttr(self):
        """Dataset: delete DICOM attribute by name.........................."""

        def testAttribute():
            ds.TreatmentMachineName

        ds = self.dummy_dataset()
        del ds.TreatmentMachineName
        self.assertRaises(AttributeError, testAttribute)

    def testDeleteOtherAttr(self):
        """Dataset: delete non-DICOM attribute by name......................"""
        ds = self.dummy_dataset()
        ds.meaningoflife = 42
        del ds.meaningoflife

    def testDeleteDicomAttrWeDontHave(self):
        """Dataset: try delete of missing DICOM attribute..................."""

        def try_delete():
            del ds.PatientName

        ds = self.dummy_dataset()
        self.assertRaises(AttributeError, try_delete)

    def testDeleteItemLong(self):
        """Dataset: delete item by tag number (long)..................."""
        ds = self.dummy_dataset()
        del ds[805961906]

    def testDeleteItemTuple(self):
        """Dataset: delete item by tag number (tuple).................."""
        ds = self.dummy_dataset()
        del ds[(12298, 178)]

    def testDeleteNonExistingItem(self):
        """Dataset: raise KeyError for non-existing item delete........"""
        ds = self.dummy_dataset()

        def try_delete():
            del ds[(16, 16)]

        self.assertRaises(KeyError, try_delete)


class DatasetElementsTests(unittest.TestCase):
    __doc__ = 'Test valid assignments of data elements'

    def setUp(self):
        self.ds = Dataset()
        self.sub_ds1 = Dataset()
        self.sub_ds2 = Dataset()

    def testSequenceAssignment(self):
        """Assignment to SQ works only if valid Sequence assigned......"""

        def try_non_Sequence():
            self.ds.ConceptCodeSequence = [
             1, 2, 3]

        msg = 'Assigning non-sequence to SQ data element did not raise error'
        self.assertRaises(TypeError, try_non_Sequence, msg=msg)
        self.ds.ConceptCodeSequence = [
         self.sub_ds1, self.sub_ds2]
        self.assertTrue(isinstance(self.ds.ConceptCodeSequence, Sequence), 'Sequence assignment did not result in Sequence type')


if __name__ == '__main__':
    unittest.main()