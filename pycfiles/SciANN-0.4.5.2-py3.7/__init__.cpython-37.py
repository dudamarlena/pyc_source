# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sciann/__init__.py
# Compiled at: 2020-04-22 14:39:27
# Size of source mod 2**32: 1706 bytes
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from . import constraints
from . import functionals
from . import models
from . import utils
from functionals.functional import Functional
from functionals.variable import Variable
from functionals.field import Field
from functionals.parameter import Parameter
from models.model import SciModel
from .constraints import Constraint, Data, Tie
from .utils import math
from utils.utilities import clear_tf_session
from utils.utilities import set_random_seed
from utils.utilities import set_floatx
__author__ = 'Ehsan Haghighat'
__email__ = 'ehsanh@mit.edu'
__copyright__ = 'Copyright 2019, Physics-Informed Deep Learning'
__credits__ = []
__url__ = 'http://github.com/sciann/sciann]'
__license__ = 'MIT'
__version__ = '0.4.5.2'
__cite__ = '@misc{haghighat2019sciann, \n    title={SciANN: A Keras wrapper for scientific computations and physics-informed deep learning using artificial neural networks}, \n    author={Haghighat, Ehsan and Juanes, Ruben}, \n    url={https://github.com/sciann/sciann.git}, \n    year={2019} \n}'
_header = '--------------------- {} {} ---------------------'.format(str.upper(__name__), str(__version__))
_footer = len(_header) * '-'
__welcome__ = '{} \n'.format(_header) + 'Please review the documentation at "https://www.sciann.com". \n' + '{} \n'.format(__cite__) + _footer
import os
if 'SCIANN_WELCOME_MSG' in os.environ.keys() and os.environ['SCIANN_WELCOME_MSG'] == '-1':
    pass
else:
    print(__welcome__)