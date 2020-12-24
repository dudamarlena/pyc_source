# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/__init__.py
# Compiled at: 2014-10-01 12:52:58
"""
The Landlab

:Package name: TheLandlab
:Version: 0.1.0
:Release date: 2013-03-24
:Authors:
  Greg Tucker,
  Nicole Gasparini,
  Erkan Istanbulluoglu,
  Daniel Hobley,
  Sai Nudurupati,
  Jordan Adams,
  Eric Hutton

:URL: http://csdms.colorado.edu/trac/landlab

:License: MIT
"""
from __future__ import absolute_import
__version__ = '0.1.5'
import os
if 'DISPLAY' not in os.environ:
    try:
        import matplotlib
    except ImportError:
        import warnings
        warnings.warn('matplotlib not found', ImportWarning)
    else:
        matplotlib.use('Agg')

from .core.model_parameter_dictionary import ModelParameterDictionary
from .core.model_parameter_dictionary import MissingKeyError, ParameterValueError
from .core.model_component import Component
from .framework.collections import Palette, Arena, NoProvidersError
from .framework.decorators import Implements, ImplementsOrRaise
from .framework.framework import Framework
from .field.scalar_data_fields import FieldError
from .grid import *
from .plot import *
from .testing.nosetester import LandlabTester
test = LandlabTester().test
bench = LandlabTester().bench