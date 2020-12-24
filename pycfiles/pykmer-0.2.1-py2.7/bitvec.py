# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/pykmer/bitvec.py
# Compiled at: 2017-01-24 00:00:38
"""
A basic fixed-size bit vector class.
"""
__docformat__ = 'restructuredtext'
import array

class bitvec():
    """A basic bit vector class."""

    def __init__(self, n):
        """
        Create a bit vector with `n` bits.
        """
        self.size = n
        self.words = (n + 63) // 64
        self.data = array.array('L', [ 0 ])

    def __len__(self):
        """Return the number of bits in the bit vector."""
        return self.size

    def __getitem__(self, i):
        """
        Get the bit at position `i`. (Positions are numbered from 0.)
        """
        w = i // 64
        b = i & 63
        return self.data[w] >> b & 1

    def __setitem__(self, i, x):
        """
        Set the bit at position `i` to the value of the least
        significant bit of `x`.
        """
        w = i // 64
        b = i & 63
        self.data[w] &= 18446744073709551615 - (1 << b)
        self.data[w] |= (x & 1) << b