# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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