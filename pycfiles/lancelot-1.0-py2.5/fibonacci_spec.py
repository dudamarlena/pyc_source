# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/lancelot/examples/fibonacci_spec.py
# Compiled at: 2009-02-14 11:58:24
"""
Some example Specs to illustrate usage with a standalone function
"""
import lancelot

def fib(ordinal=0):
    """ Simple and inefficent fibonacci generator with some type checking """
    if ordinal < 0:
        raise ValueError('fib(%r) is undefined' % ordinal)
    seed_values = {0: 1, 1: 1}
    try:
        return seed_values[ordinal]
    except KeyError:
        return fib(ordinal - 2) + fib(ordinal - 1)


@lancelot.verifiable
def specify_fib_zero_to_five():
    """ Spec(standalone-fn).standalone-fn(args).should_be(value) """
    spec = lancelot.Spec(fib)
    spec.fib(0).should_be(1)
    spec.fib(1).should_be(1)
    spec.fib(2).should_be(2)
    spec.fib(3).should_be(3)
    spec.fib(4).should_be(5)
    spec.fib(5).should_be(8)
    spec.fib(0).should_not_be(0)
    spec.fib(5).should_not_be(5)


@lancelot.verifiable
def specify_fib_with_named_ordinal():
    """ Spec(standalone-fn).standalone-fn(kwds).should_be(value) """
    spec = lancelot.Spec(fib)
    spec.fib(ordinal=0).should_be(1)
    spec.fib(ordinal=1).should_be(1)
    spec.fib(ordinal=2).should_be(2)
    spec.fib(ordinal=3).should_be(3)
    spec.fib(ordinal=4).should_be(5)
    spec.fib(ordinal=5).should_be(8)
    spec.fib(ordinal=0).should_not_be(0)
    spec.fib(ordinal=5).should_not_be(5)


@lancelot.verifiable
def specify_invalid_args_for_fib():
    """ Spec(standalone-fn).standalone-fn(args).should_raise(...) """
    spec = lancelot.Spec(fib)
    spec.fib(6).should_not_raise(Exception)
    spec.fib('a').should_raise(Exception)
    spec.fib(-1).should_raise(Exception)
    spec.fib(6).should_not_raise(TypeError)
    spec.fib('a').should_raise(TypeError)
    spec.fib(6).should_not_raise(ValueError)
    spec.fib(-1).should_raise(ValueError('fib(-1) is undefined'))
    spec.fib(-2).should_raise(ValueError('fib(-2) is undefined'))


if __name__ == '__main__':
    lancelot.verify()