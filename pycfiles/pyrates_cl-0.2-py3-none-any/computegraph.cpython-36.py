# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: E:\01_Work\15_PhD\11_Python_neural_mass_models\PyRates\pyrates\backend\computegraph.py
# Compiled at: 2020-01-06 14:08:25
# Size of source mod 2**32: 2876 bytes
__doc__ = 'This module provides the backend class that should be used to set up any backend in pyrates.\n'
from typing import Optional, Any
__author__ = 'Richard Gast'
__status__ = 'development'

class ComputeGraph(object):
    """ComputeGraph"""

    def __new__(cls, net_config: Any, vectorization: bool=True, name: Optional[str]='net0', backend: str='numpy', float_precision: str='float32', **kwargs) -> Any:
        """Instantiates operator.
        """
        if type(net_config) is str:
            net_config = net_config.apply()
        return (net_config.compile)(vectorization=vectorization, backend=backend, float_precision=float_precision, **kwargs)