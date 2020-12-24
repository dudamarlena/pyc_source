# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/test_omr/test_omr.py
# Compiled at: 2014-05-06 14:22:01
"""optical mark reader test suite

run via nosetests called from package root.

test classes::
    
    OmrTestCase            create temp dir with required source image files
    mock_exam_group        setup exam group conditions for testing single exam
    test_single_exam       test processing single exam
    test_exam_group        test exam group
    test_write_exam_group  test exam group output

"""
from pkg_resources import resource_filename
import os, glob
from random import randrange
from shutil import copytree
from unittest import TestCase
from omr.exam_group import process_exam_group, write_exam_group
from omr.exam import process_exam
from omr.forms import FORMS
PACKAGE_DIR = os.path.dirname(resource_filename('omr', ''))
TEST_DATA = os.path.join(PACKAGE_DIR, 'test_omr', 'test_data')
TEST_TEMP = os.path.join(PACKAGE_DIR, 'test_omr', 'test_tmp')

class OmrTestCase(TestCase):
    """create temp dir with required source image files"""

    @classmethod
    def setUpClass(self):
        """setup test fixture attributes (inherited by all tests)"""
        rand_hex_str = str(randrange(1000000000.0))
        self.path = os.path.join(TEST_TEMP, rand_hex_str)
        self.outdir = os.path.join(self.path, 'OMR')
        self.imfile = os.path.join(self.path, 'Image (0).jpg')
        self.form = '882E'
        self.side = 'front'
        self.formcfg = FORMS['882E']['front']
        copytree(TEST_DATA, self.path)


class mock_exam_group(OmrTestCase):
    """setup exam group conditions to test single exam processing"""

    @classmethod
    def setUpClass(self):
        """setup exam group conditions to test single exam processing"""
        super(mock_exam_group, self).setUpClass()
        for p in ['', 'validation', 'names']:
            f = os.path.join(self.outdir, p)
            if not os.path.exists(f):
                os.mkdir(f)

    def test_outpath_exists(self):
        """single exam: mock output directories created"""
        self.assertTrue(os.path.exists(self.outdir))
        self.assertTrue(os.path.exists(os.path.join(self.outdir, 'names')))
        self.assertTrue(os.path.exists(os.path.join(self.outdir, 'validation')))


class test_single_exam(mock_exam_group):
    """single exam tests"""

    @classmethod
    def setUpClass(self):
        """setup single exam test fixture"""
        super(test_single_exam, self).setUpClass()
        self.choices = process_exam(self.imfile, self.formcfg)

    def test_choice(self):
        """single exam: choices exist"""
        self.assertTrue(len(self.choices) > 0)


class test_exam_group(OmrTestCase):
    """exam group tests"""

    @classmethod
    def setUpClass(self):
        """setup exam group test fixture"""
        super(test_exam_group, self).setUpClass()
        self.images, self.choices, self.outdir = process_exam_group(self.path, self.form, self.side)

    def test_outpath_exists(self):
        """exam group: output directories created"""
        self.assertTrue(os.path.exists(self.outdir))
        self.assertTrue(os.path.exists(os.path.join(self.outdir, 'validation')))
        self.assertTrue(os.path.exists(os.path.join(self.outdir, 'names')))

    def test_validation_images_exist(self):
        """exam group: all validation images written"""
        val_images = glob.glob(os.path.join(self.outdir, 'validation', '*'))
        self.assertEqual(len(self.images), len(val_images))

    def test_name_images_exist(self):
        """exam group: all name images written"""
        name_images = glob.glob(os.path.join(self.outdir, 'names', '*'))
        self.assertEqual(len(self.images), len(name_images))


class test_write_exam_group(test_exam_group):
    """write exam group tests"""

    @classmethod
    def setUpClass(self):
        """setup write exam group test fixture"""
        super(test_write_exam_group, self).setUpClass()
        write_exam_group(self.images, self.choices, self.outdir)

    def test_output_files(self):
        """exam group: output files exist"""
        self.assertTrue(os.path.exists(os.path.join(self.outdir, 'results.xlsx')))