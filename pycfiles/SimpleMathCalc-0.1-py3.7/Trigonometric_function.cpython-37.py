# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\SimpleMathCalc\Trigonometric_function.py
# Compiled at: 2019-04-09 12:30:28
# Size of source mod 2**32: 619 bytes


def Trigonometric_function():
    number = list()
    while True:
        c = input('Input a number. Then Press the Enter key ')
        if c == 'done':
            break
        try:
            c = float(c)
        except:
            print('Please input a number!')
            continue

        import math
        print('sin(c):', math.sin(c))
        print('cos(c):', math.cos(c))
        print('tan(c):', math.tan(c))


Trigonometric_function()