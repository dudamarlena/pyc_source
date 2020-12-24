# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shliyana/anaconda3/lib/python3.7/site-packages/tests/test_htrc_volumes.py
# Compiled at: 2019-05-06 10:39:58
# Size of source mod 2**32: 5724 bytes
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import sys
if sys.version_info.major == 2:
    from mock import Mock, patch, PropertyMock
else:
    if sys.version_info.major == 3:
        from unittest.mock import Mock, patch, PropertyMock
from io import BytesIO
from tempfile import NamedTemporaryFile, mkdtemp
import unittest2 as unittest, htrc.volumes, htrc.config

class MockResponse(BytesIO):

    def __init__(self, data, status=200, *args, **kwargs):
        (BytesIO.__init__)(self, data, *args, **kwargs)
        self.status = status


class TestVolumes(unittest.TestCase):

    def setUp(self):
        self.test_vols = [
         'mdp.39015050817181', 'mdp.39015055436151',
         'mdp.39015056169157', 'mdp.39015050161697', 'mdp.39015042791874']
        self.config_path = NamedTemporaryFile(delete=False).name
        self.empty_config_path = NamedTemporaryFile(delete=False).name
        self.output_path = mkdtemp()

    def tearDown(self):
        import os, shutil
        os.remove(self.config_path)
        shutil.rmtree(self.output_path)

    @patch('htrc.volumes.http.client.HTTPSConnection')
    def test_get_volumes_and_pages(self, https_mock):
        response_mock = Mock(status=200)
        response_mock.read.return_value = ''.encode('utf8')
        https_mock.return_value.getresponse.return_value = response_mock
        htrc.volumes.get_volumes('1234', self.test_vols, 'data-host', '443', '/home/client-certs/client.pem', '/home/client-certs/client.pem', '/')
        htrc.volumes.get_pages('1234', self.test_vols, 'data-host', '443', '/home/client-certs/client.pem', '/home/client-certs/client.pem', '/')

    @patch('htrc.volumes.http.client.HTTPSConnection')
    def test_get_volumes_and_pages_error(self, https_mock):
        response_mock = Mock(status=500)
        https_mock.return_value.getresponse.return_value = response_mock
        with self.assertRaises(EnvironmentError):
            htrc.volumes.get_volumes('1234', self.test_vols, 'data-host', '443', '/home/client-certs/client.pem', '/home/client-certs/client.pem', '/')
        with self.assertRaises(EnvironmentError):
            htrc.volumes.get_pages('1234', self.test_vols, 'data-host', '443', '/home/client-certs/client.pem', '/home/client-certs/client.pem', '/')

    def test_get_volumes_and_pages_empty(self):
        with self.assertRaises(ValueError):
            htrc.volumes.get_volumes('1234', [], 'data-host', '443', '/home/client-certs/client.pem', '/home/client-certs/client.pem', '/')
        with self.assertRaises(ValueError):
            htrc.volumes.get_pages('1234', [], 'data-host', '443', '/home/client-certs/client.pem', '/home/client-certs/client.pem', '/')

    @patch('htrc.volumes.ZipFile')
    @patch('htrc.volumes.get_volumes')
    @patch('htrc.volumes.get_oauth2_token')
    @patch('htrc.volumes.http.client.HTTPSConnection')
    def test_download_volumes(self, https_mock, oauth2_mock, volumes_mock, zip_mock):
        response_mock = Mock(status=200)
        https_mock.return_value.getresponse.return_value = response_mock
        oauth2_mock.return_value = 'a1b2c3d4e5'
        volumes_mock.return_value = b''
        htrc.volumes.download_volumes((self.test_vols), (self.output_path), username='1234',
          password='1234',
          token='1234')
        import shutil
        shutil.rmtree(self.output_path)
        htrc.volumes.download_volumes((self.test_vols), (self.output_path), username='1234',
          password='1234',
          token='1234')

    def test_download(self):
        pass


suite = unittest.TestLoader().loadTestsFromTestCase(TestVolumes)
unittest.TextTestRunner(verbosity=2).run(suite)