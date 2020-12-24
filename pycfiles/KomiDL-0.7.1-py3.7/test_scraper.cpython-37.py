# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\test_scraper.py
# Compiled at: 2019-10-12 01:12:13
# Size of source mod 2**32: 9437 bytes
"""Tests the Scraper class in KomiDL"""
import os, sys, unittest
from unittest import mock
from multiprocessing.dummy import Lock
sys.path.append(os.path.abspath('..'))
from komidl.scraper import Scraper
from komidl.exceptions import ExtractorFailed, InvalidURL

class ScraperTest(unittest.TestCase):
    __doc__ = 'Tests the Scraper class in KomiDL'

    def setUp(self):
        """Create the Scraper object for usage"""
        self.scraper = Scraper(3)

    def test_change_extension(self):
        """Test the function that changes file ext for a URL"""
        url = 'http://website.com/test/image.jpg'
        ext = 'png'
        expected = 'http://website.com/test/image.png'
        actual = self.scraper._change_extension(url, ext)
        self.assertEqual(actual, expected)

    def test_get_extension(self):
        test_cases = (('img.jpg', ('img', 'jpg')), ('thing.img.gif', ('thing.img', 'gif')))
        for img, (expected_path, expected_ext) in test_cases:
            actual_path, actual_ext = self.scraper._get_extension(img)
            self.assertEqual(actual_path, expected_path)
            self.assertEqual(actual_ext, expected_ext)

    def test_build_title(self):
        test_cases = (
         (
          '[DNSHENG][EN] Some Title',
          {'Title':'Some Title', 
           'Languages':'English', 
           'Authors':'DNSheng'}),
         (
          '[PICASSO][IT] UNTITLED',
          {'Languages':[
            'Italian', 'English'], 
           'Artists':'Picasso'}),
         (
          '[UNKNOWN][JA][0001-0004] Cool stories',
          {'Title':'Cool stories', 
           'Languages':[
            'Japanese', 'English'], 
           'Chapters':'0001-0004'}),
         (
          '[MINUTEMEN][JA] A settlement needs your help',
          {'Title':'A settlement needs your help', 
           'Languages':[
            'Japanese', 'English'], 
           'Groups':'Minutemen'}),
         (
          '[BOB ROSSxPICASSO][JA] Picture gallery',
          {'Title':'Picture gallery', 
           'Languages':[
            'Japanese', 'English'], 
           'Artists':[
            'Bob Ross', 'Picasso']}),
         (
          '[SHAKESPEARE][EN] Romeo & Juliet',
          {'Title':'Romeo & Juliet', 
           'Languages':'English', 
           'Authors':'Shakespeare', 
           'Artists':'Bob Ross', 
           'Groups':'Dead Poets Society'}))
        for expected, tag_dict in test_cases:
            actual = self.scraper._build_title(tag_dict)
            self.assertEqual(actual, expected)