# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyslo/metric_client/metric_client.py
# Compiled at: 2020-04-02 17:00:28
# Size of source mod 2**32: 1018 bytes
"""Metric Client

Metric clients are used to retrieve time series data from a vairety of
sources. The MetricClient class can be inherited by provider specific derivatives.

Currently supported:
    - StackDriver
        Client library is in alpha. Using version v3:-
            https://googleapis.dev/python/monitoring/latest/gapic/v3/api.html

Planned implementations:
    - Azure Metric Service
    - Prometheus
"""
from google.cloud import monitoring_v3
MetricDescriptor = monitoring_v3.enums.MetricDescriptor

class NoMetricDataAvailable(Exception):
    __doc__ = ' NoMetricDataAvailable\n\n    Thrown if you try to retrieve data using invalid\n    or out of range parameters\n    '


class MetricClient:
    __doc__ = 'Parent object for source specific metric clients.\n\n    Attributes:\n        project:       id of the GCP project hosting Stackdriver\n\n    '
    value_type = None

    def timeseries_dataframe(self):
        """Retrieve data from time series db and return as a pandas dataframe
        """
        pass