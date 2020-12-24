# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\chartit\__init__.py
# Compiled at: 2016-09-11 22:31:24
"""
This Django application can be used to create charts and pivot charts
directly from models.
"""
from .chartdata import PivotDataPool, DataPool
from .charts import PivotChart, Chart
__version__ = '0.2.3'