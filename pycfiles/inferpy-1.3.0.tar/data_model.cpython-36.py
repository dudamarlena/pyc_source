# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/contextmanager/data_model.py
# Compiled at: 2020-02-12 04:52:06
# Size of source mod 2**32: 3052 bytes
from contextlib import contextmanager, ExitStack
from . import randvar_registry
_active_datamodel = dict(size=1,
  active=False)

def is_active():
    return _active_datamodel['active']


def _has_datamodel_var_parameters(name):
    graph = randvar_registry.get_graph()
    return any(randvar_registry.get_variable_or_parameter(pname).is_datamodel for pname in graph.predecessors(name))


def get_sample_shape(name):
    """
    This function must be used inside a datamodel context (it is not checked here)
    If the parameters are not already expanded, then are now expanded.
        :name (str): The name of the variable to get its sample shape
        :returns: the sample_shape (number of samples of the datamodel). It is an integer, or ().
    """
    if _has_datamodel_var_parameters(name):
        size = ()
    else:
        size = _active_datamodel['size']
    return size


@contextmanager
def fit(size):
    if not isinstance(size, int):
        raise TypeError('The size of the data model must be an integer, not : {}'.format(type(size)))
    _active_datamodel['size'] = size
    try:
        yield
    finally:
        _active_datamodel['size'] = 1


@contextmanager
def datamodel(size=None):
    """
    This context is used to declare a plateau model. Random Variables and Parameters will use a sample_shape
    defined by the argument `size`, or by the `data_model.fit`. If `size` is not specified, the default size 1,
    or the size specified by `fit` will be used.
    """
    assert not _active_datamodel['active']
    _active_datamodel['active'] = True
    contexts = []
    if size:
        contexts.append(fit(size))
    try:
        with ExitStack() as (stack):
            for c in contexts:
                stack.enter_context(c)

            yield
    finally:
        _active_datamodel['active'] = False