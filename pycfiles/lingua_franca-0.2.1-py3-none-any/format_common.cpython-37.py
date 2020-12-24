# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ake/projects/python/lingua-franca/lingua_franca/lang/format_common.py
# Compiled at: 2020-01-13 02:46:59
# Size of source mod 2**32: 1629 bytes


def convert_to_mixed_fraction(number, denominators=range(1, 21)):
    """
    Convert floats to components of a mixed fraction representation

    Returns the closest fractional representation using the
    provided denominators.  For example, 4.500002 would become
    the whole number 4, the numerator 1 and the denominator 2

    Args:
        number (float): number for convert
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        whole, numerator, denominator (int): Integers of the mixed fraction
    """
    int_number = int(number)
    if int_number == number:
        return (
         int_number, 0, 1)
    frac_number = abs(number - int_number)
    if not denominators:
        denominators = range(1, 21)
    for denominator in denominators:
        numerator = abs(frac_number) * denominator
        if abs(numerator - round(numerator)) < 0.01:
            break
    else:
        return

    return (
     int_number, int(round(numerator)), denominator)