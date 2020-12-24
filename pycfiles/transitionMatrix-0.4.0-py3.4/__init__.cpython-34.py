# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/transitionMatrix/__init__.py
# Compiled at: 2018-10-22 18:32:13
# Size of source mod 2**32: 1149 bytes
""" transitionMatrix - Python package for statistical analysis and visualization of state space transition events """
from .model import *
from .estimators import *
from .utils import *
from .thresholds import *
from .portfolio_model_lib import *
__version__ = '0.4.0'
package_name = 'transitionMatrix'
module_path = os.path.dirname(__file__)
source_path = module_path[:-len(package_name)]
dataset_path = os.path.join(source_path, '/datasets/')