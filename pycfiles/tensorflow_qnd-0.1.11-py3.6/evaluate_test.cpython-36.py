# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qnd/evaluate_test.py
# Compiled at: 2017-05-17 13:34:19
# Size of source mod 2**32: 197 bytes
import types
from . import evaluate
from . import test

def test_def_evaluate():
    test.append_argv('--output_dir', 'output')
    assert isinstance(evaluate.def_evaluate(), types.FunctionType)