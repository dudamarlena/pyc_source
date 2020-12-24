# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/haoda/ir/type.py
# Compiled at: 2020-05-05 13:44:06
# Size of source mod 2**32: 4283 bytes
from typing import Any, Optional
from cached_property import cached_property
import haoda.util
TYPE_WIDTH = {'float':32, 
 'double':64,  'half':16}
HAODA_TYPE_TO_CL_TYPE = {'uint8':'uchar', 
 'uint16':'ushort', 
 'uint32':'uint', 
 'uint64':'ulong', 
 'int8':'char', 
 'int16':'short', 
 'int32':'int', 
 'int64':'long', 
 'half':'half', 
 'float':'float', 
 'double':'double', 
 'float16':'half', 
 'float32':'float', 
 'float64':'double'}

class Type:

    def __init__(self, val: Optional[str]):
        if not isinstance(val, (str, type(None))):
            raise TypeError('Type can only be constructed from str or NoneType, got ' + type(val).__name__)
        self._val = val

    def __str__(self) -> str:
        return str(self._val)

    def __hash__(self) -> int:
        if self._val is None:
            return hash(None)
        else:
            return self.width_in_bits

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            other = Type(other)
        else:
            if not isinstance(other, Type):
                return NotImplemented
            self_val = self._val
            other_val = other._val
            if self.is_float:
                self_val = 'float%d' % self.width_in_bits
            if other.is_float:
                other_val = 'float%d' % other.width_in_bits
        return self_val == other_val

    @cached_property
    def c_type(self) -> Optional[str]:
        if self._val in frozenset({'int64', 'uint64', 'uint32', 'int8', 'uint8', 'uint16', 'int32', 'int16'}):
            return self._val + '_t'
        else:
            if self._val is None:
                return
            else:
                if self._val == 'float32':
                    return 'float'
                if self._val == 'float64':
                    return 'double'
            for token in ('int', 'uint'):
                if self._val.startswith(token):
                    bits = self._val.replace(token, '').split('_')
                    if len(bits) > 1:
                        assert len(bits) == 2
                        return ('ap_{}<{}, {}>'.format)(token.replace('int', 'fixed'), *bits)
                    else:
                        assert len(bits) == 1
                        return ('ap_{}<{}>'.format)(token, *bits)

            return self._val

    @cached_property
    def width_in_bits(self) -> int:
        if isinstance(self._val, str):
            if self._val in TYPE_WIDTH:
                return TYPE_WIDTH[self._val]
            for prefix in ('uint', 'int', 'float'):
                if self._val.startswith(prefix):
                    return int(self._val.lstrip(prefix).split('_')[0])

        else:
            if hasattr(self._val, 'haoda_type'):
                assert self._val is not None
                return self._val.haoda_type.width_in_bits
        raise haoda.util.InternalError('unknown haoda type: %s' % self._val)

    @cached_property
    def width_in_bytes(self) -> int:
        return (self.width_in_bits - 1) // 8 + 1

    def common_type(self, other: 'Type') -> 'Type':
        """Return the common type of two operands.

    TODO: Consider fractional.

    Args:
      lhs: Haoda type of operand 1.
      rhs: Haoda type of operand 2.

    Returns:
      The common type of two operands.
    """
        if self._val is None:
            return self
        else:
            if other._val is None:
                return other
            else:
                if self.is_float:
                    if not other.is_float:
                        return self
                if other.is_float:
                    if not self.is_float:
                        return other
                if self.width_in_bits < other.width_in_bits:
                    return other
            return self

    @cached_property
    def is_float(self) -> bool:
        if self._val is None:
            return False
        else:
            return self._val in frozenset({'double', 'half'}) or self._val.startswith('float')

    @cached_property
    def is_fixed(self) -> bool:
        if self._val is None:
            return False
        else:
            for token in ('int', 'uint'):
                if self._val.startswith(token):
                    bits = self._val.replace(token, '').split('_')
                    if len(bits) > 1:
                        return True

            return False

    @cached_property
    def cl_type(self) -> Optional[str]:
        if self._val is None:
            return
        else:
            cl_type = HAODA_TYPE_TO_CL_TYPE.get(self._val)
            if cl_type is not None:
                return cl_type
            return self._val + '_t'

    def get_cl_vec_type(self, burst_width: int) -> str:
        scalar_width = self.width_in_bits
        if not burst_width % scalar_width == 0:
            raise AssertionError('burst width must be a multiple of width of the scalar type')
        elif not self._val in HAODA_TYPE_TO_CL_TYPE:
            raise AssertionError('scalar type not supported')
        return HAODA_TYPE_TO_CL_TYPE[self._val] + str(burst_width // scalar_width)