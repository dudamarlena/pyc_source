# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/test/test_metrics_api.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 1360 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
from __future__ import absolute_import
import unittest, mux_python
from mux_python.api.metrics_api import MetricsApi
from mux_python.rest import ApiException

class TestMetricsApi(unittest.TestCase):
    __doc__ = 'MetricsApi unit test stubs'

    def setUp(self):
        self.api = mux_python.api.metrics_api.MetricsApi()

    def tearDown(self):
        pass

    def test_get_metric_timeseries_data(self):
        """Test case for get_metric_timeseries_data

        Get metric timeseries data  # noqa: E501
        """
        pass

    def test_get_overall_values(self):
        """Test case for get_overall_values

        Get Overall values  # noqa: E501
        """
        pass

    def test_list_all_metric_values(self):
        """Test case for list_all_metric_values

        List all metric values  # noqa: E501
        """
        pass

    def test_list_breakdown_values(self):
        """Test case for list_breakdown_values

        List breakdown values  # noqa: E501
        """
        pass

    def test_list_insights(self):
        """Test case for list_insights

        List Insights  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()