# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/anomaly_detection/__init__.py
# Compiled at: 2019-02-19 10:52:03
# Size of source mod 2**32: 334 bytes
"""
    anomaly_detection
    A Pure Python library of Twitter's AnomalyDetection R Package.
    :license: Apache-2.0, see LICENSE for more details.
"""
__version__ = '0.0.2'
from anomaly_detection.anomaly_detect_ts import anomaly_detect_ts
from anomaly_detection.anomaly_detect_vec import anomaly_detect_vec