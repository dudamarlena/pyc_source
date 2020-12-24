# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ploader/tests/test_utils.py
# Compiled at: 2014-01-15 12:53:58
# Size of source mod 2**32: 2326 bytes
from unittest import TestCase
import ploader.utils as utils

class TestUtils(TestCase):

    def test_size_formatting(self):
        self.assertEqual(utils.sizeof_fmt(-1), '-1.0bytes')
        self.assertEqual(utils.sizeof_fmt(0), '0.0bytes')
        self.assertEqual(utils.sizeof_fmt(1000000), '976.6KB')
        self.assertEqual(utils.sizeof_fmt(1000000000000000), '909.5TB')

    def test_url_filename_conversion(self):
        self.assertEqual(utils.url_to_filename('http://www.catb.org/jargon/html/S/schroedinbug.html'), 'schroedinbug.html')
        self.assertEqual(utils.url_to_filename('http://www.catb.org/jargon/html/S/'), '')
        self.assertEqual(utils.url_to_filename('http://www.catb.org'), '')

    def test_link_extractor(self):
        self.assertEqual(utils.clean_links('http://www.catb.org/jargon/html/S/schroedinbug.html\n'), ['http://www.catb.org/jargon/html/S/schroedinbug.html'])
        self.assertEqual(utils.clean_links('catb.org/jargon/html/S/schroedinbug.html'), [])
        self.assertEqual(utils.clean_links('http:// catb.org/jargon/html/S/schroedinbug.html'), [])
        self.assertEqual(utils.clean_links('http://www.catb.org/jargon/html/S/schroedinbug.html\nhttp://www.catb.org'), ['http://www.catb.org/jargon/html/S/schroedinbug.html', 'http://www.catb.org'])
        self.assertEqual(utils.clean_links('http://www.catb.org/jargon/html/S/schroedinbug.html http://www.catb.org'), ['http://www.catb.org/jargon/html/S/schroedinbug.html', 'http://www.catb.org'])
        self.assertEqual(utils.clean_links('http://www.catb.org/jargon/html/S/schroedinbug.html-http://www.catb.org'), ['http://www.catb.org/jargon/html/S/schroedinbug.html-http://www.catb.org'])
        self.assertEqual(utils.clean_links('https://www.catb.org/jargon/html/S/schroedinbug.html\nhttps://www.catb.org'), ['https://www.catb.org/jargon/html/S/schroedinbug.html', 'https://www.catb.org'])
        self.assertEqual(utils.clean_links('ftp://www.catb.org/jargon/html/S/schroedinbug.html\nftp://www.catb.org'), ['ftp://www.catb.org/jargon/html/S/schroedinbug.html', 'ftp://www.catb.org'])

    def test_urlinfo_parser(self):
        self.assertFalse(utils.parse_url_info('http://www.google.com/', [], '', 2))
        self.assertFalse(utils.parse_url_info('http://www.google.com', [], '', 2))
        self.assertEqual(utils.parse_url_info('http://sub.dom.net/my_tar.tar.gz', [], '', 2), ('my_tar.tar.gz',
                                                                                               'http://sub.dom.net/my_tar.tar.gz'))