# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/satella/instrumentation/metrics/metric_types/registry.py
# Compiled at: 2020-04-29 12:14:00
# Size of source mod 2**32: 313 bytes
from .base import Metric
METRIC_NAMES_TO_CLASSES = {}
__all__ = [
 'METRIC_NAMES_TO_CLASSES', 'register_metric']

def register_metric(cls):
    """
    Decorator to register your custom metrics
    """
    METRIC_NAMES_TO_CLASSES[cls.CLASS_NAME] = cls
    return cls