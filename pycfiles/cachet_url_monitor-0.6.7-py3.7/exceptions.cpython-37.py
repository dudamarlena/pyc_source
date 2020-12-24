# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/cachet_url_monitor/exceptions.py
# Compiled at: 2020-02-08 23:35:47
# Size of source mod 2**32: 809 bytes


class ComponentNonexistentError(Exception):
    __doc__ = 'Exception raised when the component does not exist.'

    def __init__(self, component_id):
        self.component_id = component_id

    def __str__(self):
        return repr(f"Component with id [{self.component_id}] does not exist.")


class MetricNonexistentError(Exception):
    __doc__ = 'Exception raised when the component does not exist.'

    def __init__(self, metric_id):
        self.metric_id = metric_id

    def __str__(self):
        return repr(f"Metric with id [{self.metric_id}] does not exist.")


class ConfigurationValidationError(Exception):
    __doc__ = "Exception raised when there's a validation error."

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)