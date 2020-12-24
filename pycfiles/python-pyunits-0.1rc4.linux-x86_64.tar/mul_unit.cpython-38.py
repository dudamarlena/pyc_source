# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.0/x64/lib/python3.8/site-packages/pyunits/compound_units/mul_unit.py
# Compiled at: 2019-11-23 19:40:19
# Size of source mod 2**32: 761 bytes
import numpy as np
from .compound_unit import CompoundUnit

class MulUnit(CompoundUnit):
    __doc__ = '\n    A pseudo-unit that is produced by a CompoundUnitType to represent a compound\n    unit comprised of the multiplication of two other units.\n    '

    @property
    def raw(self) -> np.ndarray:
        """
        See superclass for documentation.
        """
        return self.left.raw * self.right.raw

    @property
    def name(self) -> str:
        """
        See superclass for documentation.
        """
        return '{}{}'.format(self.left.name, self.right.name)