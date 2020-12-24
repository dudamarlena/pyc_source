# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/__init__.py
# Compiled at: 2019-04-01 10:58:44
# Size of source mod 2**32: 248 bytes
__version__ = '1.0.0'
from .models import *
from . import inference
from .contextmanager import datamodel
from .exceptions import *
from util.runtime import set_tf_run