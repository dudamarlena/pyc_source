# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/pbdmymath/adv/fib.py
# Compiled at: 2017-07-10 08:29:26
from math import sqrt

def fibonacci(n):
    """
    http://stackoverflow.com/questions/494594/how-to-write-the-fibonacci-sequence-in-python
    """
    return ((1 + sqrt(5)) ** n - (1 - sqrt(5)) ** n) / (2 ** n * sqrt(5))