# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/selector_unit_test.py
# Compiled at: 2010-08-05 11:04:07
"""Unit-tests various XML/CSV validation scenarios (called tests also) in 
selector.py."""
from selector import Selector, HUDHMIS28XMLTest
import unittest, os, testCase_settings, postgresutils

class SelectorTestCase(unittest.TestCase):
    """see if the return value is a file path"""

    def test_validation_valid(self):
        """Tests if HMIS XML 2.8 test is validating properly."""
        self.Wipe_DB_clean()
        select = Selector()
        instance_filename = os.path.join('%s' % testCase_settings.INPUTFILES_PATH, testCase_settings.XML_FILE_VALID)
        result = select.validate(instance_filename, False)
        print result
        self.assertEqual(result, [False, True, False])

    def test_validation_invalid(self):
        """Tests if HMIS XML 2.8 test is properly invalidating some invalid XML
        """
        self.Wipe_DB_clean()
        select = Selector()
        instance_filename = os.path.join('%s' % testCase_settings.INPUTFILES_PATH, testCase_settings.XML_FILE_INVALID)
        result = select.validate(instance_filename, False)
        print result
        self.assertEqual(result, [False, True, False])

    def test_validation_valid_n_shred(self):
        """Tests if HMIS XML 2.8 test is properly validating some valid XML and Shredding into the DB
        """
        self.Wipe_DB_clean()
        select = Selector()
        instance_filename = os.path.join('%s' % testCase_settings.INPUTFILES_PATH, testCase_settings.XML_FILE_VALID)
        result = select.validate(instance_filename, True)
        print result
        self.assertEqual(result, [False, True, False])

    def test_db_values(self):
        """ Tests to see if we have XML Data in our DB
            After shredding the XML_FILE_VALID file, our db should contain
            3 records in the [Person] table,
            2 records in [Person_Address]
        """
        self.Wipe_DB_clean()
        select = Selector()
        instance_filename = os.path.join('%s' % testCase_settings.INPUTFILES_PATH, testCase_settings.XML_FILE_VALID)
        result = select.validate(instance_filename, True)
        print result
        self.assertEqual(result, False)

    def test_validation_malformed_xml(self):
        """Tests if HMIS XML 2.8 test is properly invalidating some malformed 
        XML.  Malformed in this context means missing an end tag or some basic
        XML error.  Not a schema validation driven error."""
        self.Wipe_DB_clean()
        select = Selector()
        instance_filename = os.path.join('%s' % testCase_settings.INPUTFILES_PATH, testCase_settings.XML_FILE_MALFORMED)
        result = select.validate(instance_filename, False)
        print result
        self.assertEqual(result, [False, None, False])
        return

    def Wipe_DB_clean(self):
        UTILS = postgresutils.Utils()
        UTILS.blank_database()


if __name__ == '__main__':
    unittest.main()