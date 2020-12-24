# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Auzzy\Documents\git\pyinq\examples\eval_order.py
# Compiled at: 2013-11-12 17:24:15
from pyinq.tags import test
from pyinq.asserts import eval_equal, eval_raises

def unexpected():
    raise Exception('EXCEPTION')


def no_error():
    pass


@test
def unexpected_error_last():
    eval_equal(4, 5)
    eval_raises(IOError, unexpected)


@test
def unexpected_error_first():
    eval_raises(IOError, unexpected)
    eval_equal(4, 5)


@test
def fail_last():
    eval_equal(4, 5)
    eval_raises(IOError, no_error)


@test
def fail_first():
    eval_raises(IOError, no_error)
    eval_equal(4, 5)