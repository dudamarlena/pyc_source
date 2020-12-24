# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyslo/metric_client/stackdriver/stackdriver_filter.py
# Compiled at: 2020-04-02 17:00:28
# Size of source mod 2**32: 1713 bytes
"""Stackdriver Filter

"""

class StackDriverFilter:
    __doc__ = 'Hold variables and generate filter strings.\n\n    Args:\n        metric_type: string. e.g. composer.googleapis.com/environment/healthy\n        resource_type: string. e.g. cloud_composer_environment\n        resource_labels: Not implemented\n        metric_labels: Not implemented\n    '

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