# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shliyana/anaconda3/lib/python3.7/site-packages/tests/test_download_cli.py
# Compiled at: 2019-05-06 10:39:58
# Size of source mod 2**32: 1957 bytes
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import sys
if sys.version_info.major == 2:
    from mock import Mock, patch, PropertyMock
else:
    if sys.version_info.major == 3:
        from unittest.mock import Mock, patch, PropertyMock
import unittest2 as unittest, htrc.__main__, argparse

class TestDownload(unittest.TestCase):

    @patch('argparse._sys.argv', ['htrc', 'download', 'mdp.1234567'])
    @patch('htrc.__main__.download')
    def test_raw_volume_id(self, download_mock):
        htrc.__main__.main()
        download_mock.assert_called_once()

    @patch('argparse._sys.argv', ['htrc', 'download', '001423370'])
    @patch('htrc.__main__.download')
    def test_raw_record_id(self, download_mock):
        htrc.__main__.main()
        download_mock.assert_called_once()

    @patch('argparse._sys.argv', ['htrc', 'download', 'https://babel.hathitrust.org/cgi/pt?id=mdp.39015078560078;view=1up;seq=13'])
    @patch('htrc.__main__.download')
    def test_babel_url(self, download_mock):
        htrc.__main__.main()
        download_mock.assert_called_once()

    @patch('argparse._sys.argv', ['htrc', 'download', 'https://hdl.handle.net/2027/mdp.39015078560078'])
    @patch('htrc.__main__.download')
    def test_handle_url(self, download_mock):
        htrc.__main__.main()
        download_mock.assert_called_once()

    @patch('argparse._sys.argv', ['htrc', 'download', 'https://catalog.hathitrust.org/Record/001423370'])
    @patch('htrc.__main__.download')
    def test_catalog_url(self, download_mock):
        htrc.__main__.main()
        download_mock.assert_called_once()

    @patch('argparse._sys.argv', ['htrc', 'download', 'https://babel.hathitrust.org/shcgi/mb?a=listis;c=696632727'])
    @patch('htrc.__main__.download')
    def test_collection_builder_url(self, download_mock):
        htrc.__main__.main()
        download_mock.assert_called_once()