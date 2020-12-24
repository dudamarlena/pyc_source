# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qnd/__init__.py
# Compiled at: 2017-06-30 10:38:06
# Size of source mod 2**32: 389 bytes
"""Quick and Dirty TensorFlow command framework"""
from .flag import *
from .infer import def_infer
from .train_and_evaluate import def_train_and_evaluate
from .evaluate import def_evaluate
from .serve import def_serve
__all__ = [
 'FLAGS', 'add_flag', 'add_required_flag', 'FlagAdder',
 'def_train_and_evaluate', 'def_evaluate', 'def_infer', 'def_serve']
__version__ = '0.1.11'