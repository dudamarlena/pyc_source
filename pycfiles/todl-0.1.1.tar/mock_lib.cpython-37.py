# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/utils/testing/mock_lib.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 1276 bytes
"""Mock objects and related functions for testing."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

class MockBenchmarkLogger(object):
    __doc__ = 'This is a mock logger that can be used in dependent tests.'

    def __init__(self):
        self.logged_metric = []

    def log_metric(self, name, value, unit=None, global_step=None, extras=None):
        self.logged_metric.append({'name':name, 
         'value':float(value), 
         'unit':unit, 
         'global_step':global_step, 
         'extras':extras})