# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/truber/src/m/lithium/src/lithium/docs/examples/arithmetic/product_divides.py
# Compiled at: 2018-04-18 20:56:31
"""This tests Lithium's main "minimize" algorithm."""
import sys

def interesting(args, _temp_prefix):
    """Interesting if the product of the numbers in the file divides the argument.

    Args:
        args (str): The first parameter.
        _temp_prefix (str): The second parameter.

    Returns:
        bool: True if successful, False otherwise.
    """
    mod = int(args[0])
    filename = args[1]
    prod = 1
    with open(filename, 'r') as (input_fp):
        for line in input_fp:
            line = line.strip()
            if line.isdigit():
                prod *= int(line)

    if prod % mod == 0:
        sys.stdout.write('%d is divisible by %d\n' % (prod, mod))
        return True
    sys.stdout.write('%d is not divisible by %d\n' % (prod, mod))
    return False