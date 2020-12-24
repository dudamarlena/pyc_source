# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/test/test_errors_api.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 699 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
from __future__ import absolute_import
import unittest, mux_python
from mux_python.api.errors_api import ErrorsApi
from mux_python.rest import ApiException

class TestErrorsApi(unittest.TestCase):
    __doc__ = 'ErrorsApi unit test stubs'

    def setUp(self):
        self.api = mux_python.api.errors_api.ErrorsApi()

    def tearDown(self):
        pass

    def test_list_errors(self):
        """Test case for list_errors

        List Errors  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()