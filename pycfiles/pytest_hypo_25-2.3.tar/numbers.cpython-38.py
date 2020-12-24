# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\strategies\_internal\numbers.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 5598 bytes
import math
import hypothesis.internal.conjecture.floats as flt
import hypothesis.internal.conjecture.utils as d
from hypothesis.control import assume, reject
from hypothesis.internal.conjecture.utils import calc_label_from_name
from hypothesis.internal.floats import float_of
from hypothesis.strategies._internal.strategies import SearchStrategy

class WideRangeIntStrategy(SearchStrategy):
    distribution = d.Sampler([4.0, 8.0, 1.0, 1.0, 0.5])
    sizes = [
     8, 16, 32, 64, 128]

    def __repr__(self):
        return 'WideRangeIntStrategy()'

    def do_draw(self, data):
        size = self.sizes[self.distribution.sample(data)]
        r = data.draw_bits(size)
        sign = r & 1
        r >>= 1
        if sign:
            r = -r
        return int(r)


class BoundedIntStrategy(SearchStrategy):
    __doc__ = 'A strategy for providing integers in some interval with inclusive\n    endpoints.'

    def __init__(self, start, end):
        SearchStrategy.__init__(self)
        self.start = start
        self.end = end

    def __repr__(self):
        return 'BoundedIntStrategy(%d, %d)' % (self.start, self.end)

    def do_draw(self, data):
        return d.integer_range(data, self.start, self.end)


NASTY_FLOATS = sorted(([
 0.0,
 0.5,
 1.1,
 1.5,
 1.9,
 0.3333333333333333,
 10000000.0,
 1e-05,
 1.175494351e-38,
 2.2250738585072014e-308,
 1.7976931348623157e+308,
 3.402823466e+38,
 9007199254740992,
 0.99999,
 2.00001,
 1.192092896e-07,
 2.220446049250313e-16] + [
 math.inf, math.nan] * 5),
  key=(flt.float_to_lex))
NASTY_FLOATS = list(map(float, NASTY_FLOATS))
NASTY_FLOATS.extend([-x for x in NASTY_FLOATS])
FLOAT_STRATEGY_DO_DRAW_LABEL = calc_label_from_name('getting another float in FloatStrategy')

class FloatStrategy(SearchStrategy):
    __doc__ = 'Generic superclass for strategies which produce floats.'

    def __init__(self, allow_infinity, allow_nan, width):
        SearchStrategy.__init__(self)
        assert isinstance(allow_infinity, bool)
        assert isinstance(allow_nan, bool)
        assert width in (16, 32, 64)
        self.allow_infinity = allow_infinity
        self.allow_nan = allow_nan
        self.width = width
        self.nasty_floats = [float_of(f, self.width) for f in NASTY_FLOATS if self.permitted(f)]
        weights = [
         0.2 * len(self.nasty_floats)] + [0.8] * len(self.nasty_floats)
        self.sampler = d.Sampler(weights)

    def __repr__(self):
        return '{}(allow_infinity={}, allow_nan={}, width={})'.format(self.__class__.__name__, self.allow_infinity, self.allow_nan, self.width)

    def permitted--- This code section failed: ---

 L. 116         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'f'
                4  LOAD_GLOBAL              float
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  LOAD_ASSERT              AssertionError
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 117        14  LOAD_FAST                'self'
               16  LOAD_ATTR                allow_infinity
               18  POP_JUMP_IF_TRUE     34  'to 34'
               20  LOAD_GLOBAL              math
               22  LOAD_METHOD              isinf
               24  LOAD_FAST                'f'
               26  CALL_METHOD_1         1  ''
               28  POP_JUMP_IF_FALSE    34  'to 34'

 L. 118        30  LOAD_CONST               False
               32  RETURN_VALUE     
             34_0  COME_FROM            28  '28'
             34_1  COME_FROM            18  '18'

 L. 119        34  LOAD_FAST                'self'
               36  LOAD_ATTR                allow_nan
               38  POP_JUMP_IF_TRUE     54  'to 54'
               40  LOAD_GLOBAL              math
               42  LOAD_METHOD              isnan
               44  LOAD_FAST                'f'
               46  CALL_METHOD_1         1  ''
               48  POP_JUMP_IF_FALSE    54  'to 54'

 L. 120        50  LOAD_CONST               False
               52  RETURN_VALUE     
             54_0  COME_FROM            48  '48'
             54_1  COME_FROM            38  '38'

 L. 121        54  LOAD_FAST                'self'
               56  LOAD_ATTR                width
               58  LOAD_CONST               64
               60  COMPARE_OP               <
               62  POP_JUMP_IF_FALSE   106  'to 106'

 L. 122        64  SETUP_FINALLY        84  'to 84'

 L. 123        66  LOAD_GLOBAL              float_of
               68  LOAD_FAST                'f'
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                width
               74  CALL_FUNCTION_2       2  ''
               76  POP_TOP          

 L. 124        78  POP_BLOCK        
               80  LOAD_CONST               True
               82  RETURN_VALUE     
             84_0  COME_FROM_FINALLY    64  '64'

 L. 125        84  DUP_TOP          
               86  LOAD_GLOBAL              OverflowError
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   104  'to 104'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L. 126        98  POP_EXCEPT       
              100  LOAD_CONST               False
              102  RETURN_VALUE     
            104_0  COME_FROM            90  '90'
              104  END_FINALLY      
            106_0  COME_FROM            62  '62'

 L. 127       106  LOAD_CONST               True
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 82

    def do_draw(self, data):
        while True:
            data.start_example(FLOAT_STRATEGY_DO_DRAW_LABEL)
            i = self.sampler.sample(data)
            if i == 0:
                result = flt.draw_float(data)
            else:
                result = self.nasty_floats[(i - 1)]
                flt.write_float(data, result)
            if self.permitted(result):
                data.stop_example()
                if self.width < 64:
                    return float_of(result, self.width)
                return result
            data.stop_example(discard=True)


class FixedBoundedFloatStrategy(SearchStrategy):
    __doc__ = 'A strategy for floats distributed between two endpoints.\n\n    The conditional distribution tries to produce values clustered\n    closer to one of the ends.\n    '

    def __init__(self, lower_bound, upper_bound, width):
        SearchStrategy.__init__(self)
        assert isinstance(lower_bound, float)
        assert isinstance(upper_bound, float)
        assert 0 <= lower_bound < upper_bound
        assert math.copysign(1, lower_bound) == 1, 'lower bound may not be -0.0'
        assert width in (16, 32, 64)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.width = width

    def __repr__(self):
        return 'FixedBoundedFloatStrategy(%s, %s, %s)' % (
         self.lower_bound,
         self.upper_bound,
         self.width)

    def do_draw(self, data):
        f = self.lower_bound + (self.upper_bound - self.lower_bound) * d.fractional_float(data)
        if self.width < 64:
            try:
                f = float_of(f, self.width)
            except OverflowError:
                reject()

        assume(self.lower_bound <= f <= self.upper_bound)
        return f