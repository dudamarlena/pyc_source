# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyBabyMaker/parse.py
# Compiled at: 2019-09-09 00:13:27
# Size of source mod 2**32: 1056 bytes
__doc__ = '\nThis module provides limited functionality to extract variables from certain\ntype of C++ expressions.\n\nCurrently, supported C++ expressions includes arithmetic and boolean calculation\nand nested function calls.\n'
import re

def is_numeral(n):
    """
    Test if ``string n`` can be converted to a numeral.
    """
    try:
        float(n)
        return True
    except ValueError:
        return False


def find_all_args(s, tokens=[
 '[\\w\\d_]*\\(', '\\)', ',',
 '\\+', '-', '\\*', '/', '%',
 '&&', '\\|\\|',
 '!', '>', '<', '=']):
    """
    Find all arguments inside a C++ expression ``s``.
    """
    for t in tokens:
        s = re.sub(t, ' ', s)

    return s.split()


def find_all_vars(s, **kwargs):
    """
    Find all arguments, minus numerals, inside a C++ expression ``s``.
    """
    args = find_all_args(s, **kwargs)
    return [v for v in args if not is_numeral(v)]