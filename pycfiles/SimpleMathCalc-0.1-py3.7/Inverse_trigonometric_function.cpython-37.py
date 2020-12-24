# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\SimpleMathCalc\Inverse_trigonometric_function.py
# Compiled at: 2019-04-09 12:24:14
# Size of source mod 2**32: 552 bytes
import math

def inversetrig(function, number):
    if function == 'asin':
        result = math.asin(float(number))
        print(result)
    else:
        if function == 'acos':
            result = math.acos(float(number))
            print(result)
        else:
            if function == 'atan':
                result = math.atan(float(number))
                print(result)