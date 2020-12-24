# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dummipy/__init__.py
# Compiled at: 2015-05-18 12:51:21
from .dummipy import CategoricalDataFrame
import pandas
pandas.cDataFrame = CategoricalDataFrame
import os
__version__ = '0.0.1'
_ROOT = os.path.abspath(os.path.dirname(__file__))
cereal = pandas.read_csv(os.path.join(_ROOT, 'data', 'cereal.csv'))
cereal = CategoricalDataFrame(cereal)