# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/__init__.py
# Compiled at: 2020-02-12 04:52:06
# Size of source mod 2**32: 363 bytes
__version__ = '1.3.0'
from .util.startup import *
from .models import *
from . import inference
from .contextmanager import datamodel
from . import layers
from .util.common import floatx, set_floatx
from .util.runtime import set_tf_run
from .util.session import *