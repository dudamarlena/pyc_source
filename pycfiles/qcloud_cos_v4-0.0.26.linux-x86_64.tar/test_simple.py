# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.14/lib/python2.7/site-packages/test/test_simple.py
# Compiled at: 2018-03-19 03:53:29
from qcloud_cos.cos_request import UploadFileRequest
import unittest

class TestRequestCase(unittest.TestCase):

    def test_upload_file_request(self):
        req = UploadFileRequest('bucketname', '/a/b/c.jpg', '/tmp/a.jpg')
        self.assertEqual(req.get_local_path(), '/tmp/a.jpg')
        self.assertEqual(req.get_insert_only(), 1)