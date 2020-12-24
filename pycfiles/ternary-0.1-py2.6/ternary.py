# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ternary.py
# Compiled at: 2010-07-22 10:40:21


class Ternary(object):
    """
    Ternary-ish emulation, it looks like C-style ternary operation::

        x = a ? b : c

    In Python we would write::

        >>> x = a and b or c

    Or (rather than above, this is safe for returning Falsy values for b)::

        >>> x = (a and [b] or [c])[0]

    Or::

        >>> x = b if a else c

    Or::

        >>> x = lambda i: (b, c)[not a]

    Or::

        >>> if a:
        ...     x = b
        ... else:
        ...     x = c

    Now we can also write::

        >>> x = ternary[a:b:c]
    """
    __getitem__ = lambda s, sl: (
     sl.start and sl.stop, not sl.start and sl.step)[(not sl.start)]


ternary = Ternary()