# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/test/test_direct_uploads_api.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 1262 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
from __future__ import absolute_import
import unittest, mux_python
from mux_python.api.direct_uploads_api import DirectUploadsApi
from mux_python.rest import ApiException

class TestDirectUploadsApi(unittest.TestCase):
    __doc__ = 'DirectUploadsApi unit test stubs'

    def setUp(self):
        self.api = mux_python.api.direct_uploads_api.DirectUploadsApi()

    def tearDown(self):
        pass

    def test_cancel_direct_upload(self):
        """Test case for cancel_direct_upload

        Cancel a direct upload  # noqa: E501
        """
        pass

    def test_create_direct_upload(self):
        """Test case for create_direct_upload

        Create a new direct upload URL  # noqa: E501
        """
        pass

    def test_get_direct_upload(self):
        """Test case for get_direct_upload

        Retrieve a single direct upload's info  # noqa: E501
        """
        pass

    def test_list_direct_uploads(self):
        """Test case for list_direct_uploads

        List direct uploads  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()