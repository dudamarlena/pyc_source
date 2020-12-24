# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/contextmanager/randvar_registry.py
# Compiled at: 2019-09-03 11:37:11
# Size of source mod 2**32: 6026 bytes
from contextlib import contextmanager
from inferpy.util import tf_graph
import warnings

def restart_default():
    global _default_properties
    _default_properties = dict(build_graph=True,
      graph=(tf_graph.get_empty_graph()),
      builder_vars=(dict()),
      builder_params=(dict()),
      is_default=True)


restart_default()
_properties = _default_properties

def is_building_graph():
    global _properties
    return _properties['build_graph']


def is_default():
    return _properties['is_default']


def register_variable(rv):
    if rv.name in _properties['builder_vars'] or rv.name in _properties['builder_params']:
        if is_default():
            if rv.name not in _properties['builder_params']:
                del _properties['builder_vars'][rv.name]
                if rv.name in _properties['graph']:
                    _properties['graph'].remove_node(rv.name)
                warnings.warn('The variable {} was already defined in the default random variable registry,                 and is going to be removed. '.format(rv.name))
        else:
            raise ValueError('Random Variable names must be unique among Random Variables and Parameters.                              Detected twice: {}'.format(rv.name))
    _properties['builder_vars'][rv.name] = rv


def register_parameter(p):
    if p.name in _properties['builder_params'] or p.name in _properties['builder_vars']:
        if is_default():
            if p.name not in _properties['builder_vars']:
                del _properties['builder_params'][p.name]
                if p.name in _properties['graph']:
                    _properties['graph'].remove_node(p.name)
                warnings.warn('The parameter {} was already defined in the default random parameter registry,                 and is going to be removed. '.format(p.name))
        else:
            raise ValueError('Parameter names must be unique among Parameters and Random Variables.                              Detected twice: {}'.format(p.name))
    _properties['builder_params'][p.name] = p


def get_variable(name):
    return _properties['builder_vars'].get(name, None)


def get_variable_or_parameter(name):
    return _properties['builder_vars'].get(name, _properties['builder_params'].get(name, None))


def get_var_parameters():
    return {k:p for k, p in _properties['builder_params'].items()}


def get_graph():
    return _properties['graph']


def update_graph(rv_name=None):
    if _properties['build_graph']:
        elements_set = set(_properties['builder_vars']).union(set(_properties['builder_params']))
        if rv_name:
            elements_set.add(rv_name)
        _properties['graph'] = tf_graph.get_graph(elements_set)


@contextmanager
def init(graph=None):
    global _properties
    if not _properties['is_default']:
        raise AssertionError
    else:
        _properties = dict()
        _properties['is_default'] = False
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
        _properties = _default_properties