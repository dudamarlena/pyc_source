# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/tests/image_test.py
# Compiled at: 2017-02-08 04:42:30
"""Calxeda: image_test.py"""
import os, shutil, tempfile, unittest
from cxmanage_api.simg import get_simg_header
from cxmanage_api.tftp import InternalTftp
from cxmanage_api.tests import random_file, TestImage

class ImageTest(unittest.TestCase):
    """ Tests involving cxmanage images

    These will rely on an internally hosted TFTP server. """

    def setUp(self):
        self.tftp = InternalTftp()
        self.work_dir = tempfile.mkdtemp(prefix='cxmanage_test-')

    def tearDown(self):
        shutil.rmtree(self.work_dir)

    def test_render_to_simg(self):
        """ Test image creation and upload """
        imglen = 1024
        priority = 1
        daddr = 12345
        filename = random_file(imglen)
        contents = open(filename).read()
        image = TestImage(filename, 'RAW')
        filename = image.render_to_simg(priority, daddr)
        simg = open(filename).read()
        header = get_simg_header(simg)
        self.assertEqual(header.priority, priority)
        self.assertEqual(header.imglen, imglen)
        self.assertEqual(header.daddr, daddr)
        self.assertEqual(simg[header.imgoff:], contents)

    @staticmethod
    def test_multiple_uploads():
        """ Test to make sure FDs are being closed """
        filename = random_file(1024)
        image = TestImage(filename, 'RAW')
        for _ in xrange(2048):
            image.render_to_simg(0, 0)

        os.remove(filename)