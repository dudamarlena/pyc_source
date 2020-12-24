# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/haoxun/Data/Project/magic_parameter/tests/test_type_declearation.py
# Compiled at: 2016-04-17 03:12:55
# Size of source mod 2**32: 731 bytes
from __future__ import division, absolute_import, print_function, unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from builtins import *
from future.builtins.disabled import *
import pytest
from magic_parameter.type_declearation import *

class UserDefined(object):
    pass


def test_type_obj():
    type_decl_factory(list)
    type_decl_factory(int)
    type_decl_factory(UserDefined)


def test_nontype_obj():
    type_decl_factory(list_t(int))
    type_decl_factory(tuple_t(int))
    type_decl_factory(set_t(int))
    type_decl_factory(dict_t(int, float))
    type_decl_factory(list_t(or_decl(int, float)))