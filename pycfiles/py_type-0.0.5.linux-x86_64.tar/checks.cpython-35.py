# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.5.3/lib/python3.5/site-packages/py_type/checks.py
# Compiled at: 2017-11-12 22:10:17
# Size of source mod 2**32: 390 bytes
from py_type.output import output

def message(exp, got):
    return 'expected: ' + str(exp) + ', got: ' + str(got)


def check_set(exp, got):
    if set(exp) != set(got):
        output.error_func(message(exp, got))


def check_list(exp, got):
    bs = map(lambda e, g: e == g, exp, got)
    if not all(bs):
        output.error_func(message(exp, got))