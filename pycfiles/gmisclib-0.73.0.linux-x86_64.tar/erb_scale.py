# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/erb_scale.py
# Compiled at: 2007-08-13 06:22:59
"""ERB Perceptual frequency scale."""
import math, Num
__version__ = '$Revision: 1.6 $'

def f_to_erb(f):
    """Frequency to ERB band number.
        http://ccrma-www.stanford.edu/~jos/bbt/Equivalent_Rectangular_Bandwidth.html
        """
    return Num.log(0.00437 * f + 1) * (21.4 / math.log(10.0))


def erb_to_f(e):
    """ERB number -> frequency
        """
    return (10.0 ** (e / 21.4) - 1) / 0.00437


def ebw(e):
    """Critical bandwidth (in Hz) at frequency e (erbs)."""
    return 0.108 * erb_to_f(e) + 24.7


if __name__ == '__main__':
    print f_to_erb(51)
    print f_to_erb(149)