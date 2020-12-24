# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dev/.py3env/lib/python3.6/site-packages/tzutil/tco.py
# Compiled at: 2018-12-04 04:14:05
# Size of source mod 2**32: 1290 bytes
import sys

class TailRecurseException(Exception):

    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs


def tco(g):
    """
  This function decorates a function with tail call
  optimization. It does this by throwing an exception
  if it is it's own grandparent, and catching such
  exceptions to fake the tail call optimization.

  This function fails if the decorated
  function recurses in a non-tail context.
  """

    def func(*args, **kwargs):
        f = sys._getframe()
        if f.f_back:
            if f.f_back.f_back:
                if f.f_back.f_back.f_code == f.f_code:
                    raise TailRecurseException(args, kwargs)
        else:
            while True:
                try:
                    return g(*args, **kwargs)
                except TailRecurseException as e:
                    args = e.args
                    kwargs = e.kwargs

    func.__doc__ = g.__doc__
    return func


if __name__ == '__main__':

    @tco
    def factorial(n, acc=1):
        """calculate a factorial"""
        if n == 0:
            return acc
        else:
            return factorial(n - 1, n * acc)


    print(factorial(10000))

    @tco
    def fib(i, current=0, next=1):
        if i == 0:
            return current
        else:
            return fib(i - 1, next, current + next)


    print(fib(10000))