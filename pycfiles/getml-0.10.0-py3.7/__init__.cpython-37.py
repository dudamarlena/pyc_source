# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/getml/__init__.py
# Compiled at: 2020-03-16 07:21:38
# Size of source mod 2**32: 2500 bytes
"""
getML (https://getml.com) is a software for automated machine learning
(AutoML) with a special focus on feature engineering for relational data
and time series. The getML algorithms can produce features that are far
more advanced than what any data scientist could write by hand or what you
could accomplish using simple brute force approaches.

This is the official python client for the getML engine.

Documentation and more details at https://docs.getml.com
"""
port = 1708
from .version import __version__
__all__ = ('communication', 'data', 'database', 'datasets', 'engine', 'hyperopt', 'models',
           'predictors', 'port')
from . import communication
from . import data
from . import database
from . import datasets
from . import engine
from . import hyperopt
from . import models
from . import predictors