# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/models/contextmanager/prob_model.py
# Compiled at: 2019-02-25 04:13:09
# Size of source mod 2**32: 3468 bytes
from contextlib import contextmanager
from inferpy import exceptions
from inferpy.util import tf_graph
_properties = dict(active=False, build_graph=False, graph=None, builder_vars=None, builder_params=None)

def is_active():
    return _properties['active']


def is_building_graph():
    return _properties['build_graph']


def register_variable(rv):
    if rv.name in _properties['builder_vars'] or rv.name in _properties['builder_params']:
        raise exceptions.NotUniqueRandomVariableName('Random Variable names must be unique among Random Variables and Parameters.                 Detected twice: {}'.format(rv.name))
    _properties['builder_vars'][rv.name] = rv


def register_parameter(p):
    if p.name in _properties['builder_params'] or p.name in _properties['builder_vars']:
        raise exceptions.NotUniqueParameterName('Parameter names must be unique among Parameters and Random Variables. Detected twice: {}'.format(p.name))
    _properties['builder_params'][p.name] = p


def get_builder_variable(name):
    return _properties['builder_vars'].get(name, _properties['builder_params'].get(name, None))


def get_var_parameters():
    return _properties['builder_params']


def get_graph():
    return _properties['graph']


def update_graph(rv_name):
    if _properties['build_graph']:
        _properties['graph'] = tf_graph.get_graph(set(_properties['builder_vars']).union(set([rv_name])).union(set(_properties['builder_params'])))


@contextmanager
def builder(graph):
    assert not _properties['active']
    _properties['active'] = True
    _properties['build_graph'] = graph is None
    if _properties['build_graph']:
        _properties['graph'] = tf_graph.get_empty_graph()
    else:
        _properties['graph'] = graph
    _properties['builder_vars'] = dict()
    _properties['builder_params'] = dict()
    try:
        yield
    finally:
        _properties['active'] = False
        _properties['build_graph'] = False
        _properties['graph'] = None
        _properties['builder_vars'] = None
        _properties['builder_params'] = None