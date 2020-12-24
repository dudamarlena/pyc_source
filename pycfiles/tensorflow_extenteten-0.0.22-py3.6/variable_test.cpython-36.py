# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/variable_test.py
# Compiled at: 2017-01-06 05:01:09
# Size of source mod 2**32: 259 bytes
from .util import static_shape, static_rank
from .variable import variable

def test_variable():
    shape = [
     123, 456]
    if not static_shape(variable(shape)) == shape:
        raise AssertionError
    else:
        initial = [float(n) for n in shape]
        assert static_rank(variable(initial)) == 1