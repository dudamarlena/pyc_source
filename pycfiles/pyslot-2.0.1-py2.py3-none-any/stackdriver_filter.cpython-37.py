# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyslo/metric_client/stackdriver/stackdriver_filter.py
# Compiled at: 2020-04-02 17:00:28
# Size of source mod 2**32: 1713 bytes
__doc__ = 'Stackdriver Filter\n\n'

class StackDriverFilter:
    """StackDriverFilter"""

    def __init__(self):
        self.metric_type = None
        self.resource_type = None
        self.resource_labels = []
        self.metric_labels = []

    @property
    def string(self):
        """Create a filter string based on properties
        Args:

        Returns:
            A string that can be passed as the filter_ arg during a MetricServiceClient
            list_time_series call.  The filter specifies which time series data is being requested.
            The filter must specify a single metric type, and can additionally
            specify metric labels and other information. For example:

            metric.type = "compute.googleapis.com/instance/cpu/usage_time" AND
                metric.labels.instance_name = "my-instance-name"
        """
        filter_string = ''
        self.validate_types_set()
        if self.metric_type:
            filter_string += f'metric.type="{self.metric_type}" '
        if self.resource_type:
            filter_string += f'resource.type="{self.resource_type}" '
        return filter_string

    def validate_types_set(self):
        """Simple validation

        Checks that at least metric_type or resource_type are set.
        """
        if not self.metric_type:
            if not self.resource_type:
                raise ValueError('Either metric_type or resource_type must be set')
        return True