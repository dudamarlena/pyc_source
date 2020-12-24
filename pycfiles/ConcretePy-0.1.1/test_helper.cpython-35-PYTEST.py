# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/charman/src/concrete-python/tests/test_helper.py
# Compiled at: 2017-07-18 13:12:53
# Size of source mod 2**32: 258 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from concrete.util import read_communication_from_file

def read_test_comm():
    communication_filename = 'tests/testdata/serif_dog-bites-man.concrete'
    return read_communication_from_file(communication_filename)