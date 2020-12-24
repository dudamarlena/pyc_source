# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\H213561\Documents\sensor_outlier_detector\sensor_outlier_detector\adv\fib.py
# Compiled at: 2017-05-17 08:09:34
from math import sqrt

def fibonacci(n):
    """
    http://stackoverflow.com/questions/494594/how-to-write-the-fibonacci-sequence-in-python
    """
    return ((1 + sqrt(5)) ** n - (1 - sqrt(5)) ** n) / (2 ** n * sqrt(5))