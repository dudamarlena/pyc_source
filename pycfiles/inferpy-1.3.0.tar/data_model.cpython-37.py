# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/models/contextmanager/data_model.py
# Compiled at: 2019-02-25 04:13:09
# Size of source mod 2**32: 2323 bytes
from contextlib import contextmanager
from . import prob_model
from inferpy import exceptions
_active_datamodel = dict(size=1,
  active=False)

def is_active():
    return _active_datamodel['active']


def _is_datamodel_var_parameters(name):
    graph = prob_model.get_graph()
    return any((prob_model.get_builder_variable(pname).is_datamodel for pname in graph.predecessors(name)))


def get_sample_shape(name):
    if prob_model.is_active():
        raise _active_datamodel['active'] or AssertionError
    elif _is_datamodel_var_parameters(name):
        size = ()
    else:
        size = _active_datamodel['size']
    return size


@contextmanager
def fit(size):
    if not isinstance(size, int):
        raise exceptions.NotIntegerDataModelSize('The size of the data model must be an integer, not : {}'.format(type(size)))
    assert _active_datamodel['size'] == 1
    _active_datamodel['size'] = size
    try:
        yield
    finally:
        _active_datamodel['size'] = 1


@contextmanager
def datamodel():
    assert not _active_datamodel['active']
    _active_datamodel['active'] = True
    try:
        yield
    finally:
        _active_datamodel['active'] = False