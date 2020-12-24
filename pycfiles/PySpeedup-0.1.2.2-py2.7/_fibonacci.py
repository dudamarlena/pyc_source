# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyspeedup/algorithms/_fibonacci.py
# Compiled at: 2017-02-25 12:54:13
from pyspeedup import concurrent

@concurrent.Cache
def fibonacci(n):
    """Computes the nth Fibonacci number. For example::

        >>> map(fibonacci,range(10))
        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    Utilizes modified code from `this answer on Stack Overflow
    <http://stackoverflow.com/a/14782458/786020>`_ based upon the concept
    explained `here on Wikipedia <http://en.wikipedia.org/wiki/Fibonacci_sequence#Matrix_form>`_
    along with concurrent caching from :class:`concurrent.Cache` for
    branching and repeated parameter optimization.

    This function is mostly intended to demonstrate the uses of apply_async, and could
    easily be improved.

    """
    if n < 0:
        raise Exception('Reverse fibonacci sequence not implemented.')
    if n <= 3:
        return (0, 1, 1, 2)[n]
    else:
        half, odd = divmod(n, 2)
        if odd:
            fibonacci.apply_async(half)
            fibonacci.apply_async(half + 1)
            a = fibonacci(half)
            b = fibonacci(half + 1)
            return a * a + b * b
        fibonacci.apply_async(half - 1)
        fibonacci.apply_async(half)
        a = fibonacci(half - 1)
        b = fibonacci(half)
        return (2 * a + b) * b


if __name__ == '__main__':
    import doctest
    doctest.testmod()