# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyslo/__init__.py
# Compiled at: 2020-04-02 17:00:28
# Size of source mod 2**32: 689 bytes
"""pyslo

Module to help standardise the calculation of SLO data from metrics.

This module implements the logic defined in the
[SRE Workbook](https://landing.google.com/sre/workbook/toc/) in an
agnostic way.

In order to have SLO's reported consistently regardless of backend
timeseries database, aggregations and computations are all performed
within the module, as opposed to relying upon the backend's API
functionality.

Whilst this may not be the most efficient methodology if you know you
can exist in a single cloud environment, or utilize a single monitoring
framework, it is helpful if you are strung out over multiple clouds
and on prem environments.
"""
__version__ = '0.0.7'