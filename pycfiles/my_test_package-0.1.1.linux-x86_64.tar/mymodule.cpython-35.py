# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/my_test_package/mymodule.py
# Compiled at: 2016-03-14 06:11:25
# Size of source mod 2**32: 1346 bytes
"""A simple module with trivial functions"""

def multiply(a, b):
    """Multiply two numbers, a and b

    A simple wrapper around the python `*` operator.  Calls `a * b`.
    Multiplying two ints will return an int, otherwise float.

    :param a: the first number
    :param b: the second mumber
    :type a: int,float,...
    :type b: int,float,...
    :return: a times b
    :rtype: int,float,...

    >>> multiply(5, 5)
    25
    >>> multiply(0.2,10)
    2.0
    """
    return a * b


def multiplication_table(n):
    """Makes a multiplication table for n, n times x for x up to n

    :param n: the number
    :type n: int
    :return: the multiplication table
    :rtype: str
    """
    table = ''
    for i in range(1, n + 1):
        table += '{} times {} is {}\n'.format(n, i, multiply(n, i))

    return table.strip()


def print_multiplication_table(n):
    """Prints a multiplcation table

    :param n: the number to mulpiply by
    :type n: int
    """
    print(multiplication_table(n))


def print_twelve_times():
    """Prints the 12 times tables"""
    print_multiplication_table(12)


def add(a, b):
    """Adds two numbers

    :param a: number
    :param b: other number
    :type a: int,float,...
    :type b: int,float,...

    >>> add(1,2)
    3
    >>> add(0, 0)
    0
    >>> add(0.3, 0.7)
    1.0
    """
    return a + b