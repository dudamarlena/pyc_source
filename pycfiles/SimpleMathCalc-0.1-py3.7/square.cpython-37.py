# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\SimpleMathCalc\square.py
# Compiled at: 2019-04-02 12:15:16
# Size of source mod 2**32: 587 bytes


def function():
    number1 = eval(input('Enter the number of squares opened: '))
    number2 = eval(input('Enter the number of squares: '))
    n = 1
    if number1 == 0:
        if number2 == 0:
            sum = 'input error'
            return sum
    elif number2 % 2 == 0 and m == n / number2:
        if number1 < 0:
            sum = 'input error'
            return sum
        sum = pow(number1, m)
        return sum
    else:
        m = n / number2
        sum = pow(number1, m)
        return sum


while True:
    print(function())