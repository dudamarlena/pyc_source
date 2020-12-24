# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\validation.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 3864 bytes
import decimal, math
from numbers import Rational, Real
from hypothesis.errors import InvalidArgument
from hypothesis.internal.coverage import check_function

@check_function
def check_type(typ, arg, name=''):
    if name:
        name += '='
    if not isinstance(arg, typ):
        if isinstance(typ, tuple):
            assert len(typ) >= 2, 'Use bare type instead of len-1 tuple'
            typ_string = 'one of %s' % ', '.join((t.__name__ for t in typ))
        else:
            typ_string = typ.__name__
        raise InvalidArgument('Expected %s but got %s%r (type=%s)' % (
         typ_string, name, arg, type(arg).__name__))


@check_function
def check_valid_integer(value):
    """Checks that value is either unspecified, or a valid integer.

    Otherwise raises InvalidArgument.
    """
    if value is None:
        return
    check_type(int, value)


@check_function
def check_valid_bound(value, name):
    """Checks that value is either unspecified, or a valid interval bound.

    Otherwise raises InvalidArgument.
    """
    if value is None or isinstance(value, (int, Rational)):
        return
    if not isinstance(value, (Real, decimal.Decimal)):
        raise InvalidArgument('%s=%r must be a real number.' % (name, value))
    if math.isnan(value):
        raise InvalidArgument('Invalid end point %s=%r' % (name, value))


@check_function
def check_valid_magnitude(value, name):
    """Checks that value is either unspecified, or a non-negative valid
    interval bound.

    Otherwise raises InvalidArgument.
    """
    check_valid_bound(value, name)
    if value is not None:
        if value < 0:
            raise InvalidArgument('%s=%r must not be negative.' % (name, value))


@check_function
def try_convert--- This code section failed: ---

 L.  79         0  LOAD_FAST                'value'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  80         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L.  81        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'value'
               16  LOAD_FAST                'typ'
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L.  82        22  LOAD_FAST                'value'
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'

 L.  83        26  SETUP_FINALLY        38  'to 38'

 L.  84        28  LOAD_FAST                'typ'
               30  LOAD_FAST                'value'
               32  CALL_FUNCTION_1       1  ''
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY    26  '26'

 L.  85        38  DUP_TOP          
               40  LOAD_GLOBAL              TypeError
               42  LOAD_GLOBAL              ValueError
               44  LOAD_GLOBAL              ArithmeticError
               46  BUILD_TUPLE_3         3 
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    90  'to 90'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L.  86        58  LOAD_GLOBAL              InvalidArgument

 L.  87        60  LOAD_STR                 'Cannot convert %s=%r of type %s to type %s'

 L.  88        62  LOAD_FAST                'name'
               64  LOAD_FAST                'value'
               66  LOAD_GLOBAL              type
               68  LOAD_FAST                'value'
               70  CALL_FUNCTION_1       1  ''
               72  LOAD_ATTR                __name__
               74  LOAD_FAST                'typ'
               76  LOAD_ATTR                __name__
               78  BUILD_TUPLE_4         4 

 L.  87        80  BINARY_MODULO    

 L.  86        82  CALL_FUNCTION_1       1  ''
               84  RAISE_VARARGS_1       1  'exception instance'
               86  POP_EXCEPT       
               88  JUMP_FORWARD         92  'to 92'
             90_0  COME_FROM            50  '50'
               90  END_FINALLY      
             92_0  COME_FROM            88  '88'

Parse error at or near `POP_TOP' instruction at offset 54


@check_function
def check_valid_size(value, name):
    """Checks that value is either unspecified, or a valid non-negative size
    expressed as an integer.

    Otherwise raises InvalidArgument.
    """
    if value is None:
        if name != 'min_size':
            return
    check_type(int, value, name)
    if value < 0:
        raise InvalidArgument('Invalid size %s=%r < 0' % (name, value))


@check_function
def check_valid_interval(lower_bound, upper_bound, lower_name, upper_name):
    """Checks that lower_bound and upper_bound are either unspecified, or they
    define a valid interval on the number line.

    Otherwise raises InvalidArgument.
    """
    if lower_bound is None or upper_bound is None:
        return
    if upper_bound < lower_bound:
        raise InvalidArgument('Cannot have %s=%r < %s=%r' % (
         upper_name, upper_bound, lower_name, lower_bound))


@check_function
def check_valid_sizes(min_size, max_size):
    check_valid_size(min_size, 'min_size')
    check_valid_size(max_size, 'max_size')
    check_valid_interval(min_size, max_size, 'min_size', 'max_size')