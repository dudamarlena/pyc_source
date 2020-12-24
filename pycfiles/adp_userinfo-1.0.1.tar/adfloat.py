# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ADPY/ADFUN/adfloat.py
# Compiled at: 2013-11-25 05:46:29
__doc__ = ' \n    Copyright 2013 Oliver Schnabel\n    \n    This file is part of ADPY.\n    ADPY is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    any later version.\n\n    ADPY is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with ADPY.  If not, see <http://www.gnu.org/licenses/>.\n'
from __future__ import division
import numpy as np

class adfloat:

    def __init__(self, value, parentfoo=None, idd=None):
        self.real = value
        self.parentfoo = parentfoo
        if idd:
            self.idd = idd
        else:
            self.idd = 'ID' + str(id(self))

    def __repr__(self):
        return self.idd

    def __set__(self, value):
        self.real = value

    def op(self, operation, other=None):
        if other:
            AA = adfloat(operation(self.real, other.real), parentfoo=self.parentfoo)
        else:
            AA = adfloat(operation(self.real), parentfoo=self.parentfoo)
        sol = self.parentfoo.add_step(operation, [self, other], AA)
        return sol

    def __sub__(self, other):
        return self.op(np.subtract, other)

    def __rsub__(self, other):
        return self.op(np.float.__rsub__, other)

    def __add__(self, other):
        return self.op(np.add, other)

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        return self.op(np.multiply, other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        return self.op(np.divide, other)

    def __rdiv__(self, other):
        return self.op(np.float.__rdiv__, other)

    def __pow__(self, other):
        return self.op(np.power, other)

    def __rpow__(self, other):
        return self.op(np.float.__rpow__, other)

    def __neg__(self):
        return self.op(np.negative)

    def cos(self):
        return self.op(np.cos)

    def sin(self):
        return self.op(np.sin)

    def tan(self):
        return self.op(np.tan)

    def exp(self):
        return self.op(np.exp)

    def arcsin(self):
        return self.op(np.arcsin)

    def arccos(self):
        return self.op(np.arccos)

    def arctan(self):
        return self.op(np.arctan)

    def sqrt(self):
        return self.op(np.sqrt)

    def log(self):
        return self.op(np.log)

    def log10(self):
        return self.op(np.log10)

    __truediv__ = __div__
    __rtruediv__ = __rdiv__