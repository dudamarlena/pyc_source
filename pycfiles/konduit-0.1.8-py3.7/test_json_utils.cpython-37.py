# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/test_json_utils.py
# Compiled at: 2020-05-07 09:38:33
# Size of source mod 2**32: 1015 bytes
import pytest
from konduit import *
from konduit.json_utils import *

@pytest.mark.unit
def test_empty_dict_type():
    d1 = empty_type_dict(InferenceConfiguration())
    d2 = {'type': 'InferenceConfiguration'}
    assert d1 == d2


@pytest.mark.unit
def test_dict_wrapper():
    d = {'foo': {'bar': 'baz'}}
    dw = DictWrapper(d)
    assert d == dw.as_dict()


@pytest.mark.unit
def test_list_wrapper():
    lst = ['a', 'b', 'c']
    lw = ListWrapper(lst)
    assert lw == lw.as_dict()
    assert lst == lw.as_list()
    x = ''
    for i in lw:
        x = i

    assert x == 'c'


@pytest.mark.unit
def test_as_dict_checker():

    class FooCallable(object):

        def __init__(self):
            pass

        def as_dict(self):
            pass

    class FooNotCallable(object):

        def __init__(self):
            self.as_dict = {}

    has_as_dict_attribute(FooCallable())
    with pytest.raises(Exception):
        has_as_dict_attribute(FooNotCallable())