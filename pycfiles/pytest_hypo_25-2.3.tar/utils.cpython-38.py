# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\conjecture\utils.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 14025 bytes
import enum, hashlib, heapq, sys
from collections import OrderedDict, abc
from fractions import Fraction
from hypothesis.errors import InvalidArgument
from hypothesis.internal.compat import bit_length, floor, int_from_bytes, qualname, str_to_bytes
from hypothesis.internal.floats import int_to_float
LABEL_MASK = 18446744073709551615

def calc_label_from_name(name):
    hashed = hashlib.sha384(str_to_bytes(name)).digest()
    return int_from_bytes(hashed[:8])


def calc_label_from_cls(cls):
    return calc_label_from_name(qualname(cls))


def combine_labels(*labels):
    label = 0
    for l in labels:
        label = label << 1 & LABEL_MASK
        label ^= l
    else:
        return label


INTEGER_RANGE_DRAW_LABEL = calc_label_from_name('another draw in integer_range()')
BIASED_COIN_LABEL = calc_label_from_name('biased_coin()')
SAMPLE_IN_SAMPLER_LABLE = calc_label_from_name('a sample() in Sampler')
ONE_FROM_MANY_LABEL = calc_label_from_name('one more from many()')

def integer_range(data, lower, upper, center=None):
    if not lower <= upper:
        raise AssertionError
    else:
        if lower == upper:
            data.draw_bits(1, forced=0)
            return int(lower)
            if center is None:
                center = lower
            else:
                center = min(max(center, lower), upper)
                if center == upper:
                    above = False
                else:
                    if center == lower:
                        above = True
                    else:
                        above = boolean(data)
                if above:
                    gap = upper - center
                else:
                    gap = center - lower
            assert gap > 0
            bits = bit_length(gap)
            probe = gap + 1
            if bits > 24 and data.draw_bits(3):
                idx = Sampler([4.0, 8.0, 1.0, 1.0, 0.5]).sample(data)
                sizes = [8, 16, 32, 64, 128]
                bits = min(bits, sizes[idx])
        else:
            while probe > gap:
                data.start_example(INTEGER_RANGE_DRAW_LABEL)
                probe = data.draw_bits(bits)
                data.stop_example(discard=(probe > gap))

            if above:
                result = center + probe
            else:
                result = center - probe
        assert lower <= result <= upper
    return int(result)


def check_sample(values, strategy_name):
    if 'numpy' in sys.modules and isinstance(values, sys.modules['numpy'].ndarray):
        if values.ndim != 1:
            raise InvalidArgument('Only one-dimensional arrays are supported for sampling, and the given value has {ndim} dimensions (shape {shape}).  This array would give samples of array slices instead of elements!  Use np.ravel(values) to convert to a one-dimensional array, or tuple(values) if you want to sample slices.'.format(ndim=(values.ndim),
              shape=(values.shape)))
    elif not isinstance(values, (OrderedDict, abc.Sequence, enum.EnumMeta)):
        raise InvalidArgument('Cannot sample from {values}, not an ordered collection. Hypothesis goes to some length to ensure that the {strategy} strategy has stable results between runs. To replay a saved example, the sampled values must have the same iteration order on every run - ruling out sets, dicts, etc due to hash randomisation. Most cases can simply use `sorted(values)`, but mixed types or special values such as math.nan require careful handling - and note that when simplifying an example, Hypothesis treats earlier values as simpler.'.format(values=(repr(values)),
          strategy=strategy_name))
    return tuple(values)


def choice(data, values):
    return values[integer_range(data, 0, len(values) - 1)]


FLOAT_PREFIX = 4607182418800017408
FULL_FLOAT = int_to_float(FLOAT_PREFIX | 18014398509481983) - 1

def fractional_float(data):
    return (int_to_float(FLOAT_PREFIX | data.draw_bits(52)) - 1) / FULL_FLOAT


def boolean(data):
    return bool(data.draw_bits(1))


def biased_coin(data, p):
    """Return True with probability p (assuming a uniform generator),
    shrinking towards False."""
    data.start_example(BIASED_COIN_LABEL)
    while True:
        if p <= 0:
            data.draw_bits(1, forced=0)
            result = False
            break
        else:
            if p >= 1:
                data.draw_bits(1, forced=1)
                result = True
                break
            falsey = floor(256 * (1 - p))
            truthy = floor(256 * p)
            remainder = 256 * p - truthy
            if falsey + truthy == 256:
                if isinstance(p, Fraction):
                    m = p.numerator
                    n = p.denominator
                else:
                    m, n = p.as_integer_ratio()
                assert n & n - 1 == 0, n
                assert n > m > 0
                truthy = m
                falsey = n - m
                bits = bit_length(n) - 1
                partial = False
            else:
                bits = 8
            partial = True
        i = data.draw_bits(bits)
        if partial and i == 255:
            p = remainder
        else:
            if falsey == 0:
                result = True
                break
            if truthy == 0:
                result = False
                break
            if i <= 1:
                result = bool(i)
                break
            result = i > falsey
            break

    data.stop_example()
    return result


class Sampler:
    __doc__ = "Sampler based on Vose's algorithm for the alias method. See\n    http://www.keithschwarz.com/darts-dice-coins/ for a good explanation.\n\n    The general idea is that we store a table of triples (base, alternate, p).\n    base. We then pick a triple uniformly at random, and choose its alternate\n    value with probability p and else choose its base value. The triples are\n    chosen so that the resulting mixture has the right distribution.\n\n    We maintain the following invariants to try to produce good shrinks:\n\n    1. The table is in lexicographic (base, alternate) order, so that choosing\n       an earlier value in the list always lowers (or at least leaves\n       unchanged) the value.\n    2. base[i] < alternate[i], so that shrinking the draw always results in\n       shrinking the chosen element.\n    "

    def __init__(self, weights):
        n = len(weights)
        self.table = [[
         i, None, None] for i in range(n)]
        total = sum(weights)
        num_type = type(total)
        zero = num_type(0)
        one = num_type(1)
        small = []
        large = []
        probabilities = [w / total for w in weights]
        scaled_probabilities = []
        for i, p in enumerate(probabilities):
            scaled = p * n
            scaled_probabilities.append(scaled)
            if scaled == 1:
                self.table[i][2] = zero
            elif scaled < 1:
                small.append(i)
            else:
                large.append(i)
        else:
            heapq.heapify(small)
            heapq.heapify(large)
            while True:
                while small and large:
                    lo = heapq.heappop(small)
                    hi = heapq.heappop(large)
                    assert lo != hi
                    assert scaled_probabilities[hi] > one
                    assert self.table[lo][1] is None
                    self.table[lo][1] = hi
                    self.table[lo][2] = one - scaled_probabilities[lo]
                    scaled_probabilities[hi] = scaled_probabilities[hi] + scaled_probabilities[lo] - one
                    if scaled_probabilities[hi] < 1:
                        heapq.heappush(small, hi)

                if scaled_probabilities[hi] == 1:
                    self.table[hi][2] = zero
                else:
                    heapq.heappush(large, hi)

            while True:
                if large:
                    self.table[large.pop()][2] = zero

            while small:
                self.table[small.pop()][2] = zero

            for entry in self.table:
                assert entry[2] is not None
                if entry[1] is None:
                    entry[1] = entry[0]
            else:
                if entry[1] < entry[0]:
                    entry[0], entry[1] = entry[1], entry[0]
                    entry[2] = one - entry[2]
                self.table.sort()

    def sample(self, data):
        data.start_example(SAMPLE_IN_SAMPLER_LABLE)
        i = integer_range(data, 0, len(self.table) - 1)
        base, alternate, alternate_chance = self.table[i]
        use_alternate = biased_coin(data, alternate_chance)
        data.stop_example()
        if use_alternate:
            return alternate
        return base


class many:
    __doc__ = 'Utility class for collections. Bundles up the logic we use for "should I\n    keep drawing more values?" and handles starting and stopping examples in\n    the right place.\n\n    Intended usage is something like:\n\n    elements = many(data, ...)\n    while elements.more():\n        add_stuff_to_result()\n    '

    def __init__--- This code section failed: ---

 L. 349         0  LOAD_CONST               0
                2  LOAD_FAST                'min_size'
                4  DUP_TOP          
                6  ROT_THREE        
                8  COMPARE_OP               <=
               10  POP_JUMP_IF_FALSE    30  'to 30'
               12  LOAD_FAST                'average_size'
               14  DUP_TOP          
               16  ROT_THREE        
               18  COMPARE_OP               <=
               20  POP_JUMP_IF_FALSE    30  'to 30'
               22  LOAD_FAST                'max_size'
               24  COMPARE_OP               <=
               26  POP_JUMP_IF_TRUE     36  'to 36'
               28  JUMP_FORWARD         32  'to 32'
             30_0  COME_FROM            20  '20'
             30_1  COME_FROM            10  '10'
               30  POP_TOP          
             32_0  COME_FROM            28  '28'
               32  LOAD_GLOBAL              AssertionError
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L. 350        36  LOAD_FAST                'min_size'
               38  LOAD_FAST                'self'
               40  STORE_ATTR               min_size

 L. 351        42  LOAD_FAST                'max_size'
               44  LOAD_FAST                'self'
               46  STORE_ATTR               max_size

 L. 352        48  LOAD_FAST                'data'
               50  LOAD_FAST                'self'
               52  STORE_ATTR               data

 L. 353        54  LOAD_CONST               1
               56  LOAD_CONST               1.0
               58  LOAD_CONST               1
               60  LOAD_FAST                'average_size'
               62  BINARY_ADD       
               64  BINARY_TRUE_DIVIDE
               66  BINARY_SUBTRACT  
               68  LOAD_FAST                'self'
               70  STORE_ATTR               stopping_value

 L. 354        72  LOAD_CONST               0
               74  LOAD_FAST                'self'
               76  STORE_ATTR               count

 L. 355        78  LOAD_CONST               0
               80  LOAD_FAST                'self'
               82  STORE_ATTR               rejections

 L. 356        84  LOAD_CONST               False
               86  LOAD_FAST                'self'
               88  STORE_ATTR               drawn

 L. 357        90  LOAD_CONST               False
               92  LOAD_FAST                'self'
               94  STORE_ATTR               force_stop

 L. 358        96  LOAD_CONST               False
               98  LOAD_FAST                'self'
              100  STORE_ATTR               rejected

Parse error at or near `None' instruction at offset -1

    def more(self):
        """Should I draw another element to add to the collection?"""
        if self.drawn:
            self.data.stop_example(discard=(self.rejected))
        else:
            self.drawn = True
            self.rejected = False
            self.data.start_example(ONE_FROM_MANY_LABEL)
            if self.min_size == self.max_size:
                should_continue = self.count < self.min_size
            else:
                if self.force_stop:
                    should_continue = False
                else:
                    if self.count < self.min_size:
                        p_continue = 1.0
                    else:
                        if self.count >= self.max_size:
                            p_continue = 0.0
                        else:
                            p_continue = self.stopping_value
                    should_continue = biased_coin(self.data, p_continue)
        if should_continue:
            self.count += 1
            return True
        self.data.stop_example()
        return False

    def reject(self):
        """Reject the last example (i.e. don't count it towards our budget of
        elements because it's not going to go in the final collection)."""
        if not self.count > 0:
            raise AssertionError
        else:
            self.count -= 1
            self.rejections += 1
            self.rejected = True
            if self.rejections > max(3, 2 * self.count):
                if self.count < self.min_size:
                    self.data.mark_invalid()
                else:
                    self.force_stop = True