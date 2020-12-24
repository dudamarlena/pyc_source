# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/numericOutputChecker.py
# Compiled at: 2019-07-15 23:56:54
from builtins import range

class NumericExample:
    """
    The actual result (3.141592653589793) differs from the given result,
    but the difference is less than 1e-6, so it still passes::

        >>> 1.5707963267948966 * 2 # doctest: +NUMERIC6
        3.14159285

    The text pieces between the numbers are also compared, performing
    white-space normalization::

        >>> ['a', 4.5, 6.9] # doctest: +NUMERIC6
        ['a', 4.5,       6.9000000001]

    Intervals in the notation emitted by sage are allows::

        >>> print("4.5?e-1") # doctest: +NUMERIC6
        4.50000000001?e-1

    """
    pass


import doctest, re, decimal
NUMERIC_LIST = []
NUMERIC_DICT = {}
ALL_NUMERIC = 0

def init_precisions(precisions):
    """
    Register flags for given precisions with doctest module.

    Unfortunately, doctest doesn't seem to support a more generic mechanism
    such as "# doctest: +NUMERIC: 6" to specify the precision and we need to
    unroll each precision we want to its own flag.
    """
    global ALL_NUMERIC
    global NUMERIC_DICT
    global NUMERIC_LIST
    for precision in precisions:
        if precision not in NUMERIC_DICT:
            flag = doctest.register_optionflag('NUMERIC%d' % precision)
            NUMERIC_LIST.append((precision, flag))
            NUMERIC_DICT[precision] = flag
            ALL_NUMERIC |= flag


init_precisions(range(0, 33, 3))

def get_precision(optionflags):
    """
    Get precision from optionflags
    """
    for precision, flag in NUMERIC_LIST:
        if optionflags & flag:
            return precision


mantissa_pat = '([0-9]+(?:\\.[0-9]+)?)'
interval_pat = '(\\?)?'
exponent_pat = '(?:\\ ?([eE][+-]?[0-9]+))?'
number_re = re.compile('(' + mantissa_pat + interval_pat + exponent_pat + ')')
number_group_count = 4
number_split_stride = number_group_count + 1
NUMERIC_DEFAULT_OPTIONFLAGS = doctest.NORMALIZE_WHITESPACE

def to_decimal(groups):
    number, mantissa, interval, exponent = groups
    if exponent:
        n = mantissa + exponent
    else:
        n = mantissa
    return decimal.Decimal(n)


class NumericOutputChecker(doctest.OutputChecker):
    r"""
    Implements doctest's OutputChecker, see documentation of
    NumericExample for examples.

    >>> N = NumericOutputChecker()

    >>> a   = "[3.499e-8, 4.5?e-8]"
    >>> b   = "[3.499e-8,   4.5?e-8]"

    >>> N.check_output(a, b, NUMERIC_DICT[12])
    True

    >>> b   = "[3.499999e-8,   3.2?e-8]"
    >>> N.check_output(a, b, NUMERIC_DICT[6])
    True
    >>> N.check_output(a, b, NUMERIC_DICT[9])
    False
    >>> N.formatted_compare_numeric(a, b, NUMERIC_DICT[9])
    'Numbers differed by 1.3E-8\n\nExpected     : 3.499e-8\nGot          : 3.499999e-8\nDifference          : 9.99E-12\n\nExpected     : 4.5?e-8\nGot          : 3.2?e-8\nDifference (FAILURE): 1.3E-8\n'
    >>> N.compare_numeric(a, b, NUMERIC_DICT[12])
    ('NUMERIC', ([('3.499e-8', '3.499999e-8', True, Decimal('9.99E-12')), ('4.5?e-8', '3.2?e-8', True, Decimal('1.3E-8'))], Decimal('1.3E-8')))

    >>> b   = "[3.4999e-8,  4.5e-8]"
    >>> N.formatted_compare_numeric(a, b, NUMERIC_DICT[6])
    'Expected interval, but got 4.5e-8.'

    >>> b   = "[3.4999?e-8, 4.5e-8]"
    >>> N.formatted_compare_numeric(a, b, NUMERIC_DICT[6])
    'Expected number, but got 3.4999?e-8.'

    >>> b  = "a = [3.4999e-8,  4.5?e-8]"
    >>> N.formatted_compare_numeric(a, b, NUMERIC_DICT[6])
    'Text between numbers differs'

    >>> b  = "[3.4999e-8,  4.5?e-8, 5.63]"
    >>> N.formatted_compare_numeric(a, b, NUMERIC_DICT[6])
    'Expected 2 numbers but got 3 numbers.'

    >>> a   = "[4.5,       6.7e1,       2e+3]"
    >>> b   = "[4.5000001, 67.00000001, 2.0000000000000000001e+3]"
    >>> N.compare_numeric(a, b, NUMERIC_DICT[6])
    ('OK', None)
    >>> N.compare_numeric(a, b, NUMERIC_DICT[12])    
    ('NUMERIC', ([('4.5', '4.5000001', True, Decimal('1E-7')), ('6.7e1', '67.00000001', True, Decimal('1E-8')), ('2e+3', '2.0000000000000000001e+3', False, Decimal('1E-16'))], Decimal('1E-7')))

    Account for pari adding a space before the E::

    >>> a   = "4.5e-9"
    >>> b   = "4.5 E-9"
    >>> N.compare_numeric(a, b, NUMERIC_DICT[12])
    ('OK', None)

    """

    def compare_numeric(self, want, got, optionflags):
        """
        Compares want and got by scanning for numbers. The numbers are
        compared using an epsilon extracted from optionflags. The text
        pieces between the numbers are compared falling back to the
        default implementation of OutputChecker.

        Returns a pair (status, data) where status is 'OK' if the
        comparison passed or indicates how it failed with data containing
        information that can be used to format the text explaining the
        differences.
        """
        split_want = re.split(number_re, want)
        split_got = re.split(number_re, got)
        if len(split_want) != len(split_got):
            return ('COUNT',
             (
              len(split_want) // number_split_stride,
              len(split_got) // number_split_stride))
        else:
            flags = optionflags | NUMERIC_DEFAULT_OPTIONFLAGS
            for i in range(0, len(split_want), number_split_stride):
                if not doctest.OutputChecker.check_output(self, split_want[i], split_got[i], flags):
                    return ('TEXT', None)

            epsilon = decimal.Decimal(0.1) ** get_precision(optionflags)
            rows = []
            max_diff = 0
            for i in range(1, len(split_want), number_split_stride):
                number_want = split_want[i]
                number_got = split_got[i]
                is_interval_want = bool(split_want[(i + 2)])
                is_interval_got = bool(split_got[(i + 2)])
                if is_interval_want != is_interval_got:
                    return ('TYPE', (is_interval_want, number_got))
                decimal_want = to_decimal(split_want[i:i + number_group_count])
                decimal_got = to_decimal(split_got[i:i + number_group_count])
                diff = abs(decimal_want - decimal_got)
                failed = diff > epsilon
                max_diff = max(max_diff, diff)
                rows.append((number_want, number_got, failed, diff))

            if max_diff > epsilon:
                return (
                 'NUMERIC', (rows, max_diff))
            return ('OK', None)

    def format_compare_numeric_result(self, status, data):
        """
        Formats a nice text from the result of compare_numeric.
        """
        if status == 'COUNT':
            return 'Expected %d numbers but got %d numbers.' % data
        if status == 'TEXT':
            return 'Text between numbers differs'
        if status == 'TYPE':
            is_interval_want, number_got = data
            if is_interval_want:
                k = 'interval'
            else:
                k = 'number'
            return 'Expected %s, but got %s.' % (k, number_got)
        if status == 'NUMERIC':
            rows, max_diff = data
            result = 'Numbers differed by %s\n' % max_diff
            for number_want, number_got, failed, diff in rows:
                if result:
                    result += '\n'
                result += 'Expected     : %s\n' % number_want
                result += 'Got          : %s\n' % number_got
                if failed:
                    result += 'Difference (FAILURE): %s\n' % diff
                else:
                    result += 'Difference          : %s\n' % diff

            return result
        raise Exception('Internal error in OutputChecker.')

    def formatted_compare_numeric(self, want, got, optionflags):
        """
        Performs comparison of compare_numeric and returns formatted
        text.

        Only supposed to be used if comparison failed.
        """
        status, data = self.compare_numeric(want, got, optionflags)
        return self.format_compare_numeric_result(status, data)

    def check_output(self, want, got, optionflags):
        """
        Implementation of OutputChecker method.
        """
        if want == got:
            return True
        else:
            if optionflags & ALL_NUMERIC:
                status, data = self.compare_numeric(want, got, optionflags)
                return status == 'OK'
            return doctest.OutputChecker.check_output(self, want, got, optionflags)

    def output_difference(self, example, got, optionflags):
        """
        Implementation of OutputChecker method.
        """
        if not optionflags & ALL_NUMERIC or example.exc_msg:
            return doctest.OutputChecker.output_difference(self, example, got, optionflags)
        else:
            flags = optionflags | NUMERIC_DEFAULT_OPTIONFLAGS
            base_result = doctest.OutputChecker.output_difference(self, example, got, flags)
            compare_result = self.formatted_compare_numeric(example.want, got, optionflags)
            return base_result + '\nReason for failure: ' + compare_result + '\n'


def run_doctests(verbose=False):
    failed, attempted = (0, 0)
    finder = doctest.DocTestFinder()
    runner = doctest.DocTestRunner(verbose=verbose)
    for test in finder.find(NumericOutputChecker):
        runner.run(test)

    result = runner.summarize()
    failed += result.failed
    attempted += result.attempted
    runner = doctest.DocTestRunner(checker=NumericOutputChecker(), verbose=verbose)
    for test in finder.find(NumericExample):
        runner.run(test)
        result = runner.summarize()
        failed += result.failed
        attempted += result.attempted

    return doctest.TestResults(failed, attempted)


run_doctests.__name__ = 'NumericOutputChecker'