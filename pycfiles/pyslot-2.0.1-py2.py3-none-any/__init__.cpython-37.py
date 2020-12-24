# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyslo/__init__.py
# Compiled at: 2020-04-02 17:00:28
# Size of source mod 2**32: 689 bytes
__doc__ = "pyslo\n\nModule to help standardise the calculation of SLO data from metrics.\n\nThis module implements the logic defined in the\n[SRE Workbook](https://landing.google.com/sre/workbook/toc/) in an\nagnostic way.\n\nIn order to have SLO's reported consistently regardless of backend\ntimeseries database, aggregations and computations are all performed\nwithin the module, as opposed to relying upon the backend's API\nfunctionality.\n\nWhilst this may not be the most efficient methodology if you know you\ncan exist in a single cloud environment, or utilize a single monitoring\nframework, it is helpful if you are strung out over multiple clouds\nand on prem environments.\n"
__version__ = '0.0.7'