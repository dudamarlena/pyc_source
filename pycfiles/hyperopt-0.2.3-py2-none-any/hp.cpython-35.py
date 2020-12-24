# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/max/code/oss/hyperopt/hyperopt/hp.py
# Compiled at: 2019-10-17 07:38:06
# Size of source mod 2**32: 710 bytes
"""
Support nicer user syntax:
    from hyperopt import hp
    hp.uniform('x', 0, 1)
"""
from __future__ import absolute_import
from .pyll_utils import hp_choice as choice
from .pyll_utils import hp_randint as randint
from .pyll_utils import hp_pchoice as pchoice
from .pyll_utils import hp_uniform as uniform
from .pyll_utils import hp_uniformint as uniformint
from .pyll_utils import hp_quniform as quniform
from .pyll_utils import hp_loguniform as loguniform
from .pyll_utils import hp_qloguniform as qloguniform
from .pyll_utils import hp_normal as normal
from .pyll_utils import hp_qnormal as qnormal
from .pyll_utils import hp_lognormal as lognormal
from .pyll_utils import hp_qlognormal as qlognormal