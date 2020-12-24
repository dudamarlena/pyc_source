# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/charman/src/concrete-python/tests/test_helper.py
# Compiled at: 2017-07-18 13:12:53
# Size of source mod 2**32: 258 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from concrete.util import read_communication_from_file

def read_test_comm():
    communication_filename = 'tests/testdata/serif_dog-bites-man.concrete'
    return read_communication_from_file(communication_filename)