# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\floats.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 3874 bytes
import math, struct
from hypothesis.internal.compat import CAN_PACK_HALF_FLOAT
STRUCT_FORMATS = {16:(b'!H', b'!e'), 
 32:(b'!I', b'!f'), 
 64:(b'!Q', b'!d')}

def reinterpret_bits(x, from_, to):
    return struct.unpack(to, struct.pack(from_, x))[0]


if not CAN_PACK_HALF_FLOAT:
    try:
        import numpy
    except ImportError:
        pass
    else:

        def reinterpret_bits(x, from_, to):
            if from_ == b'!e':
                arr = numpy.array([x], dtype='>f2')
                if numpy.isfinite(x):
                    if not numpy.isfinite(arr[0]):
                        raise OverflowError('%r too large for float16' % (x,)) from None
                buf = arr.tobytes()
            else:
                buf = struct.pack(from_, x)
            if to == b'!e':
                return float(numpy.frombuffer(buf, dtype='>f2')[0])
            return struct.unpack(to, buf)[0]


def float_of(x, width):
    assert width in (16, 32, 64)
    if width == 64:
        return float(x)
    if width == 32:
        return reinterpret_bits(float(x), b'!f', b'!f')
    return reinterpret_bits(float(x), b'!e', b'!e')


def sign--- This code section failed: ---

 L.  68         0  SETUP_FINALLY        16  'to 16'

 L.  69         2  LOAD_GLOBAL              math
                4  LOAD_METHOD              copysign
                6  LOAD_CONST               1.0
                8  LOAD_FAST                'x'
               10  CALL_METHOD_2         2  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.  70        16  DUP_TOP          
               18  LOAD_GLOBAL              TypeError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    56  'to 56'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  71        30  LOAD_GLOBAL              TypeError
               32  LOAD_STR                 'Expected float but got %r of type %s'
               34  LOAD_FAST                'x'
               36  LOAD_GLOBAL              type
               38  LOAD_FAST                'x'
               40  CALL_FUNCTION_1       1  ''
               42  LOAD_ATTR                __name__
               44  BUILD_TUPLE_2         2 
               46  BINARY_MODULO    
               48  CALL_FUNCTION_1       1  ''
               50  RAISE_VARARGS_1       1  'exception instance'
               52  POP_EXCEPT       
               54  JUMP_FORWARD         58  'to 58'
             56_0  COME_FROM            22  '22'
               56  END_FINALLY      
             58_0  COME_FROM            54  '54'

Parse error at or near `POP_TOP' instruction at offset 26


def is_negative(x):
    return sign(x) < 0


def count_between_floats(x, y, width=64):
    if not x <= y:
        raise AssertionError
    elif is_negative(x):
        if is_negative(y):
            return float_to_int(x, width) - float_to_int(y, width) + 1
        return count_between_floats(x, -0.0, width) + count_between_floats(0.0, y, width)
    else:
        assert not is_negative(y)
        return float_to_int(y, width) - float_to_int(x, width) + 1


def float_to_int(value, width=64):
    fmt_int, fmt_flt = STRUCT_FORMATS[width]
    return reinterpret_bits(value, fmt_flt, fmt_int)


def int_to_float(value, width=64):
    fmt_int, fmt_flt = STRUCT_FORMATS[width]
    return reinterpret_bits(value, fmt_int, fmt_flt)


def next_up(value, width=64):
    """Return the first float larger than finite `val` - IEEE 754's `nextUp`.

    From https://stackoverflow.com/a/10426033, with thanks to Mark Dickinson.
    """
    if not isinstance(value, float):
        raise AssertionError
    elif not math.isnan(value):
        if math.isinf(value):
            if value > 0:
                return value
        if value == 0.0:
            if is_negative(value):
                return 0.0
        fmt_int, fmt_flt = STRUCT_FORMATS[width]
        fmt_int = fmt_int.lower()
        n = reinterpret_bits(value, fmt_flt, fmt_int)
        if n >= 0:
            n += 1
    else:
        n -= 1
    return reinterpret_bits(n, fmt_int, fmt_flt)


def next_down(value, width=64):
    return -next_up(-value, width)