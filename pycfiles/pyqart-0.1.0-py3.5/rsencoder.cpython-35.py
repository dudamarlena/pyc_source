# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyqart/qr/ec/rsencoder.py
# Compiled at: 2017-05-03 05:33:45
# Size of source mod 2**32: 1199 bytes
from .poly import GF28Poly
from ...common import Bits

class _RSGenPolynomials(object):

    def __init__(self):
        self._table = [
         None, GF28Poly.from_index_list([0, 0], 1)]

    def __getitem__(self, index):
        while index > len(self._table) - 1:
            c = len(self._table) - 1
            self._table.append(self._table[(-1)] * GF28Poly.from_index_list([0, c], 1))

        return self._table[index]


RSGenPolynomials = _RSGenPolynomials()

class RSEncoder(object):

    @classmethod
    def encode(cls, data, ec_length, need_bits=True):
        assert ec_length >= 0
        if ec_length == 0:
            return Bits()
        else:
            if not isinstance(data, list):
                data = data.as_int_list
            data_length = len(data)
            all_length = ec_length + data_length
            m = GF28Poly.from_value_list(data + [0] * ec_length, all_length - 1)
            g = RSGenPolynomials[ec_length]
            r = m % g
            res = r.as_int_list
            if len(res) < ec_length:
                res = [
                 0] * (ec_length - len(res)) + res
            if need_bits:
                return Bits.copy_from(bytearray(res))
            return res