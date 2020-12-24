# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.0/x64/lib/python3.8/site-packages/pyunits/types.py
# Compiled at: 2019-11-23 19:40:19
# Size of source mod 2**32: 709 bytes
from typing import Any, Iterable, NamedTuple, Type, Union
import numpy as np
Numeric = Union[(np.ndarray, int, float, Iterable)]
UnitValue = Union[('unit_interface.UnitInterface', Numeric)]
RequestType = Any

class CompoundTypeFactories(NamedTuple):
    __doc__ = '\n    Enumerates the CompoundUnitType classes we want to use for creating compound\n    units.\n    :param mul_type: The multiplication type.\n    :param div_type: The division type.\n    '
    mul: Type
    div: Type