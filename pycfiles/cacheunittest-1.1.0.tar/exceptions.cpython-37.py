# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/cachet_url_monitor/exceptions.py
# Compiled at: 2020-02-08 23:35:47
# Size of source mod 2**32: 809 bytes


class ComponentNonexistentError(Exception):
    """ComponentNonexistentError"""

    def __init__(self, component_id):
        self.component_id = component_id

    def __str__(self):
        return repr(f"Component with id [{self.component_id}] does not exist.")


class MetricNonexistentError(Exception):
    """MetricNonexistentError"""

    def __init__(self, metric_id):
        self.metric_id = metric_id

    def __str__(self):
        return repr(f"Metric with id [{self.metric_id}] does not exist.")


class ConfigurationValidationError(Exception):
    """ConfigurationValidationError"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)