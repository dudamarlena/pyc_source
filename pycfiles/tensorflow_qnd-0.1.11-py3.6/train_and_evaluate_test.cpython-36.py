# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qnd/train_and_evaluate_test.py
# Compiled at: 2017-05-17 13:34:19
# Size of source mod 2**32: 252 bytes
import types
from .experiment_test import append_argv
from . import train_and_evaluate

def test_def_train_and_evaluate():
    append_argv()
    assert isinstance(train_and_evaluate.def_train_and_evaluate(), types.FunctionType)