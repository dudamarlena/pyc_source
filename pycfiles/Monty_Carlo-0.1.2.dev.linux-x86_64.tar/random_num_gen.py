# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/monty-carlo/random_num_gen/random_num_gen.py
# Compiled at: 2011-09-08 12:15:17
"""
Created on Aug 12, 2011

@author: mali, ege
"""
import numpy as num, datetime, profile

def random_number(k):
    """
    generates a uniform list consisting of 
    2**(k-2) numbers in random order in the
    interval [0,1] 

    our recursion is in the following form:
    x_n+1=x_n * rho (mod 2**k)
    we work in base 2 and we drop the last
    2 digits of each element(again in base 
    2) and then convert it to decimal, so
    we will have each number from 0 to 
    2**(k-2) once in a shuffled order then
    by dividing each element by 2**(k-2)
    we will have a uniform list in the
    interval [0,1] 

    (since it is lengthy and harder to go
    from binary <--> decimal couple of
    times in this code we extend the same
    logic such that we can use the same algorithm
    using the decimal representation only, details
    can be found in the comments)

    when rho=8t-3 our list is 
    guaranteed to have a period of 2**(k-2)
        
    """
    now = datetime.datetime.now()
    x = num.zeros(2 ** (k - 2), num.float64)
    rand_num = num.zeros(2 ** (k - 2), num.float64)
    rand_num_normal = num.zeros(2 ** (k - 2), num.float64)
    rand_num_bin = '0'
    t = now.second
    x[0] = (2 * t + 3) % 2 ** k
    if t != 0:
        rho = 8 * t - 3
    else:
        rho = 3
    for n in range(2 ** (k - 2) - 1):
        x[n + 1] = x[n] * rho % 2 ** k

    for n in range(2 ** (k - 2)):
        rand_num[n] = (x[n] - x[n] % 4) / 4
        rand_num_normal[n] = rand_num[n] / (2 ** (k - 2) - 1)

    return rand_num_normal


def bigloop():
    randoms = []
    for stack in range(100):
        randoms = num.append(randoms, random_number(15))
        print stack

    return randoms