# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyslo/metric_client/metric_client.py
# Compiled at: 2020-04-02 17:00:28
# Size of source mod 2**32: 1018 bytes
__doc__ = 'Metric Client\n\nMetric clients are used to retrieve time series data from a vairety of\nsources. The MetricClient class can be inherited by provider specific derivatives.\n\nCurrently supported:\n    - StackDriver\n        Client library is in alpha. Using version v3:-\n            https://googleapis.dev/python/monitoring/latest/gapic/v3/api.html\n\nPlanned implementations:\n    - Azure Metric Service\n    - Prometheus\n'
from google.cloud import monitoring_v3
MetricDescriptor = monitoring_v3.enums.MetricDescriptor

class NoMetricDataAvailable(Exception):
    """NoMetricDataAvailable"""
    pass


class MetricClient:
    """MetricClient"""
    value_type = None

    def timeseries_dataframe(self):
        """Retrieve data from time series db and return as a pandas dataframe
        """
        pass