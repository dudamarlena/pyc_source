# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington_core/print_util.py
# Compiled at: 2020-04-04 11:50:41
# Size of source mod 2**32: 446 bytes
import math

def to_relevant_precision(a):
    if a == 0:
        return (0, 0)
    precision = 0
    abs_a = math.fabs(a)
    while abs_a < 1.0:
        abs_a *= 10
        precision += 1

    if a < 0:
        return (
         -abs_a, precision)
    return (
     abs_a, precision)


def to_precise_string(a, n):
    new_a, precision = to_relevant_precision(a)
    if precision < 3:
        return f"{a:.{n + precision}f}"
    return f"{new_a:.{n}f}e-0{precision}"