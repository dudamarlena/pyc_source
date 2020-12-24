# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\01_Work\15_PhD\11_Python_neural_mass_models\PyRates\pyrates\backend\computegraph.py
# Compiled at: 2020-01-06 14:08:25
# Size of source mod 2**32: 2876 bytes
"""This module provides the backend class that should be used to set up any backend in pyrates.
"""
from typing import Optional, Any
__author__ = 'Richard Gast'
__status__ = 'development'

class ComputeGraph(object):
    __doc__ = 'Creates a compute graph that contains all nodes in the network plus their recurrent connections.\n\n    Parameters\n    ----------\n    net_config\n        Intermediate representation of the network configuration. For a more detailed description, see the documentation\n        of `pyrates.IR.CircuitIR`.\n    step_size\n        Step-size with which the network should be simulated later on.\n        Important for discretizing delays, differential equations, ...\n    vectorization\n        Defines the mode of automatic parallelization optimization that should be used. Can be `nodes` for lumping all\n        nodes together in a vector, `full` for full vectorization of the network, or `None` for no vectorization.\n    name\n        Name of the network.\n    backend\n        Backend in which to build the compute graph.\n    solver\n        Numerical solver to use for differential equations.\n\n    '

    def __new__(cls, net_config: Any, vectorization: bool=True, name: Optional[str]='net0', backend: str='numpy', float_precision: str='float32', **kwargs) -> Any:
        """Instantiates operator.
        """
        if type(net_config) is str:
            net_config = net_config.apply()
        return (net_config.compile)(vectorization=vectorization, backend=backend, float_precision=float_precision, **kwargs)