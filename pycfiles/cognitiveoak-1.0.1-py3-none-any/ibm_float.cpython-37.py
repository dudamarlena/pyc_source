# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\src\segpy\ibm_float.py
# Compiled at: 2019-12-13 22:18:41
# Size of source mod 2**32: 14993 bytes
from math import frexp, isnan, isinf, ceil, floor, trunc
from numbers import Real
import os, sys
sys.path.append(os.path.dirname(__file__)[:-6][:-4][:-13])
from cognitivegeo.src.segpy.util import four_bytes
IBM_ZERO_BYTES = '\x00\x00\x00\x00'
IBM_NEGATIVE_ONE_BYTES = b'\xc1\x10\x00\x00'
IBM_POSITIVE_ONE_BYTES = 'A\x10\x00\x00'
MIN_IBM_FLOAT = -7.2370051459731155e+75
LARGEST_NEGATIVE_NORMAL_IBM_FLOAT = -5.397605346934028e-79
SMALLEST_POSITIVE_NORMAL_IBM_FLOAT = 5.397605346934028e-79
MAX_IBM_FLOAT = 7.2370051459731155e+75
MAX_BITS_PRECISION_IBM_FLOAT = 24
MIN_BITS_PRECISION_IBM_FLOAT = 21
EPSILON_IBM_FLOAT = pow(2.0, -(MIN_BITS_PRECISION_IBM_FLOAT - 1))
_L24 = 2 ** MAX_BITS_PRECISION_IBM_FLOAT
_F24 = float(pow(2, MAX_BITS_PRECISION_IBM_FLOAT))
_L21 = 2 ** MIN_BITS_PRECISION_IBM_FLOAT
EXPONENT_BIAS = 64
MIN_EXACT_INTEGER_IBM_FLOAT = -2 ** MAX_BITS_PRECISION_IBM_FLOAT
MAX_EXACT_INTEGER_IBM_FLOAT = 2 ** MIN_BITS_PRECISION_IBM_FLOAT

def ibm2ieee(big_endian_bytes):
    """Interpret a byte string as a big-endian IBM float.

    Args:
        big_endian_bytes (str): A string containing at least four bytes.

    Returns:
        The floating point value.
    """
    a, b, c, d = four_bytes(big_endian_bytes)
    if a == b  == c == d == 0:
        return 0.0
    sign = -1 if a & 128 else 1
    exponent_16_biased = a & 127
    mantissa = (b << 16 | c << 8 | d) / _F24
    value = sign * mantissa * pow(16, exponent_16_biased - EXPONENT_BIAS)
    return value


BITS_PER_NYBBLE = 4

def truncate(big_endian_bytes):
    a, b, c, d = four_bytes(big_endian_bytes)
    sign = -1 if a & 128 else 1
    exponent_16_biased = a & 127
    exponent_16 = exponent_16_biased - EXPONENT_BIAS
    mantissa = b << 16 | c << 8 | d
    print('sign =', sign)
    print('exponent_16', exponent_16, hex(exponent_16), bin(exponent_16))
    print('mantissa', mantissa, hex(mantissa), bin(mantissa))
    num_nybbles_to_preserve = min(exponent_16, MAX_BITS_PRECISION_IBM_FLOAT // BITS_PER_NYBBLE)
    num_bits_to_clear = MAX_BITS_PRECISION_IBM_FLOAT - num_nybbles_to_preserve * BITS_PER_NYBBLE
    clear_mask = 2 ** num_bits_to_clear - 1
    preserve_mask = 2 ** MAX_BITS_PRECISION_IBM_FLOAT - 1 & ~clear_mask
    print('num_nybbles_to_preserve', num_nybbles_to_preserve)
    print('num_bits_to_clear', num_bits_to_clear)
    print('clear_mask   ', bin(clear_mask))
    print('preserve_mask', bin(preserve_mask))
    truncated_mantissa = mantissa & preserve_mask
    value = truncated_mantissa * pow(16, exponent_16)
    scaled_value = value >> MAX_BITS_PRECISION_IBM_FLOAT
    return scaled_value


def ieee2ibm(f):
    """Convert a float to four big-endian bytes representing an IBM float.

    Args:
        f (float): The value to be converted.

    Returns:
        A bytes object (Python 3) or a string (Python 2) containing four
        bytes representing a big-endian IBM float.

    Raises:
        OverflowError: If f is outside the representable range.
        ValueError: If f is NaN or infinite.
        FloatingPointError: If f cannot be represented without total loss of precision.
    """
    if f == 0:
        return '\x00\x00\x00\x00'
    else:
        if isnan(f):
            raise ValueError('NaN cannot be represented in IBM floating point')
        if isinf(f):
            raise ValueError('Infinities cannot be represented in IBM floating point')
        if f < MIN_IBM_FLOAT:
            raise OverflowError('IEEE Floating point value {} is less than the representable minimum for IBM floats.'.format(f))
        if f > MAX_IBM_FLOAT:
            raise OverflowError('IEEE Floating point value {} is greater than the representable maximum for IBM floats'.format(f))
        m, e = frexp(f)
        mantissa = abs(int(m * _L24))
        exponent = e
        sign = 128 if f < 0 else 0
        remainder = exponent % 4
        if remainder != 0:
            shift = 4 - remainder
            mantissa >>= shift
            exponent += shift
        exponent_16 = exponent >> 2
        exponent_16_biased = exponent_16 + 64
        if exponent_16_biased < 0:
            shift_16 = 0 - exponent_16_biased
            exponent_16_biased += shift_16
            mantissa >>= 4 * shift_16
            if mantissa == 0:
                raise FloatingPointError('IEEE Floating point value {} is smaller than the smallest subnormal number for IBM floats.'.format(f))
    a = sign | exponent_16_biased
    b = mantissa >> 16 & 255
    c = mantissa >> 8 & 255
    d = mantissa & 255
    return bytes((a, b, c, d))


class IBMFloat(Real):
    __slots__ = [
     '_data']
    _INTERNED = {IBM_ZERO_BYTES: None, 
     IBM_NEGATIVE_ONE_BYTES: None, 
     IBM_POSITIVE_ONE_BYTES: None}

    def __new__(cls, b):
        obj = object.__new__(cls)
        data = bytes(b)
        num_bytes = len(data)
        if num_bytes != 4:
            raise ValueError('{} cannot be constructed from {} values'.format(cls.__name__, num_bytes))
        obj._data = data
        if data in cls._INTERNED:
            if cls._INTERNED[data] is None:
                cls._INTERNED[data] = obj
            return cls._INTERNED[data]
        return obj

    @classmethod
    def from_float(cls, f):
        """Construct an IBMFloat from an IEEE float.

        Args:
            f (float): The value to be converted.

        Returns:
            An IBMFloat.

        Raises:
            OverflowError: If f is outside the representable range.
            ValueError: If f is NaN or infinite.
            FloatingPointError: If f cannot be represented without total loss of precision.
        """
        return cls(ieee2ibm(f))

    @classmethod
    def from_real(cls, f):
        if isinstance(f, IBMFloat):
            return f
        return cls.from_float(f)

    @classmethod
    def from_bytes(cls, b):
        return cls(b)

    @classmethod
    def ldexp(cls, fraction, exponent):
        """Make an IBMFloat from fraction and exponent.

        The is the inverse function of IBMFloat.frexp()

        Args:
            fraction: A Real in the range -1.0 to 1.0.
            exponent: An integer in the range -256 to 255 inclusive.
        """
        if not -1.0 <= fraction <= 1.0:
            raise ValueError('ldexp fraction {!r} out of range -1.0 to +1.0')
        if not -256 <= exponent < 256:
            raise ValueError('ldexp exponent {!r} out of range -256 to 256')
        ieee = fraction * 2 ** exponent
        return IBMFloat.from_float(ieee)

    @property
    def signbit(self):
        """True if the value is negative, otherwise False."""
        return bool(self._data[0] & 128)

    def __float__(self):
        return ibm2ieee(self._data)

    def __bytes__(self):
        return self._data

    def __repr__(self):
        return '{}.from_float({!r}) ~{!r}'.format(self.__class__.__name__, self._data, float(self))

    def __str__(self):
        return str(float(self))

    def __bool__(self):
        return not self.is_zero()

    def is_zero(self):
        return self.int_mantissa == 0

    def __nonzero__(self):
        return not self.is_zero()

    def is_subnormal(self):
        if self.is_zero():
            return not all((b == 0 for b in self._data))
        return self._data[1] < 16

    def zero_subnormal(self):
        if self.is_subnormal():
            return IBM_FLOAT_ZERO
        return self

    def frexp(self):
        """Obtain the fraction and exponent.

        Returns:
            A pair where the first item is the fraction in the range -1.0 and +1.0 and the
            exponent is an integer such that f = fraction * 2**exponent
        """
        sign = -1 if self.signbit else 1
        mantissa = sign * self.int_mantissa / _F24
        exp_2 = self.exp16 * 4
        return (
         mantissa, exp_2)

    def __pos__(self):
        return self

    def __neg__(self):
        if self.is_zero():
            return IBM_FLOAT_ZERO
        data = self._data
        return IBMFloat((data[0] ^ 128,
         data[1],
         data[2],
         data[3]))

    def __abs__(self):
        if self.is_zero():
            return IBM_FLOAT_ZERO
        data = self._data
        return IBMFloat((data[0] & 127,
         data[1],
         data[2],
         data[3]))

    def __eq__(self, rhs):
        lhs = self
        if not isinstance(rhs, IBMFloat):
            return float(lhs) == float(rhs)
        lhs_sign = lhs.signbit
        rhs_sign = rhs.signbit
        if lhs_sign != rhs_sign:
            return False
        nlhs = lhs.normalize()
        nrhs = rhs.normalize()
        if not nlhs.is_subnormal():
            if not nrhs.is_subnormal():
                return nlhs._data == nrhs._data
        lhs_exp16 = nlhs.exp16
        rhs_exp16 = nrhs.exp16
        lhs_mantissa = nlhs.int_mantissa
        rhs_mantissa = nrhs.int_mantissa
        if lhs_exp16 < rhs_exp16:
            delta_exp16 = rhs_exp16 - lhs_exp16
            lhs_mantissa >>= 4 * delta_exp16
            lhs_exp16 += delta_exp16
        if lhs_exp16 > rhs_exp16:
            delta_exp16 = lhs_exp16 - rhs_exp16
            rhs_mantissa >>= 4 * delta_exp16
            rhs_exp16 += delta_exp16
        assert lhs_exp16 == rhs_exp16
        return lhs_mantissa == rhs_mantissa

    def __floordiv__(self, rhs):
        return float(self) // float(rhs)

    def __rfloordiv__(self, lhs):
        return float(lhs) // float(self)

    def __rtruediv__(self, lhs):
        q = float(lhs) / float(self)
        if isinstance(lhs, float):
            return IBMFloat.from_float(q)
        return q

    def __pow__(self, exponent):
        p = pow(float(self), float(exponent))
        if isinstance(exponent, IBMFloat):
            return IBMFloat.from_float(p)
        return p

    def __rpow__(self, base):
        return IBMFloat.from_float(pow(float(base), float(self)))

    def __mod__(self, rhs):
        m = float(self) % float(rhs)
        if isinstance(rhs, IBMFloat):
            return IBMFloat.from_float(m)
        return m

    def __rmod__(self, lhs):
        m = float(lhs) % float(self)
        if isinstance(lhs, IBMFloat):
            return IBMFloat.from_float(m)
        return m

    def __rmul__(self, lhs):
        p = float(lhs) * float(self)
        if isinstance(lhs, IBMFloat):
            return IBMFloat.from_float(p)
        return p

    def __radd__(self, lhs):
        s = float(lhs) + float(self)
        if isinstance(lhs, IBMFloat):
            return IBMFloat.from_float(s)
        return s

    def __lt__(self, rhs):
        return float(self) < float(rhs)

    def __le__(self, rhs):
        return float(self) <= float(rhs)

    def __gt__(self, rhs):
        return float(self) > float(rhs)

    def __ge__(self, rhs):
        return float(self) >= float(rhs)

    def __ceil__(self):
        t = trunc(self)
        if self.signbit:
            return t
        return t + 1

    def __floor__(self):
        t = trunc(self)
        if self.signbit:
            return t - 1
        return t

    @property
    def exp16(self):
        """The base 16 exponent."""
        exponent_16_biased = self._data[0] & 127
        exponent_16 = exponent_16_biased - EXPONENT_BIAS
        return exponent_16

    @property
    def int_mantissa(self):
        data = self._data
        return data[1] << 16 | data[2] << 8 | data[3]

    def __trunc__(self):
        sign = -1 if self.signbit else 1
        exponent_16 = self.exp16
        mantissa = self.int_mantissa
        num_nybbles_to_preserve = min(exponent_16, MAX_BITS_PRECISION_IBM_FLOAT // BITS_PER_NYBBLE)
        num_bits_to_clear = MAX_BITS_PRECISION_IBM_FLOAT - num_nybbles_to_preserve * BITS_PER_NYBBLE
        clear_mask = 2 ** num_bits_to_clear - 1
        preserve_mask = 2 ** MAX_BITS_PRECISION_IBM_FLOAT - 1 & ~clear_mask
        truncated_mantissa = mantissa & preserve_mask
        magnitude = truncated_mantissa * pow(16, exponent_16) >> MAX_BITS_PRECISION_IBM_FLOAT
        return sign * magnitude

    def normalize(self):
        """Normalize the floating point value.

        Returns:
            A normalized IBMFloat equal in value to this object.

        Raises:
            FloatingPointError: If the number could not be normalized.
        """
        if self.is_zero():
            return IBM_FLOAT_ZERO
        exponent_16 = self.exp16
        mantissa = self.int_mantissa
        while mantissa < 1048576:
            new_exponent_16 = exponent_16 - 1
            if not -64 <= new_exponent_16 < 64:
                raise FloatingPointError('Could not normalize {!r} without causing exponent overflow.'.format(self))
            mantissa <<= 4
            exponent_16 = new_exponent_16

        exponent_16_biased = exponent_16 + EXPONENT_BIAS
        sign = int(self.signbit) << 7
        a = sign | exponent_16_biased
        b = mantissa >> 16 & 255
        c = mantissa >> 8 & 255
        d = mantissa & 255
        return IBMFloat.from_bytes((a, b, c, d))

    def __round__(self, ndigits=None):
        return IBMFloat.from_float(round(float(self), ndigits))

    def __truediv__(self, rhs):
        q = float(self) / float(rhs)
        if isinstance(rhs, IBMFloat):
            return IBMFloat.from_float(q)
        return q

    def __mul__(self, rhs):
        p = float(self) * float(rhs)
        if isinstance(rhs, IBMFloat):
            return IBMFloat.from_float(p)
        return p

    def __add__(self, rhs):
        p = float(self) + float(rhs)
        if isinstance(rhs, IBMFloat):
            return IBMFloat.from_float(p)
        return p

    def __int__(self):
        return trunc(self)


IBM_FLOAT_ZERO = IBMFloat.from_bytes(IBM_ZERO_BYTES)