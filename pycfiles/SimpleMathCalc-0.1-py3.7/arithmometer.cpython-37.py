# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\SimpleMathCalc\arithmometer.py
# Compiled at: 2019-04-09 12:20:54
# Size of source mod 2**32: 2688 bytes


def function(operation):
    try:
        a = 0
        sum = 0
        if operation == 'add':
            number = int(input('How many numbers do you want：'))
            while a < number:
                x = float(input('Input number：'))
                a += 1
                sum = x + sum

            return sum
        if operation == 'minus':
            number = int(input('How many substraction：'))
            x = float(input('Input subtracted：'))
            if number == 0:
                sum = x
            else:
                sum = x
                while a < number:
                    y = eval(input('Input subtraction：'))
                    a += 1
                    sum = sum - y

            return sum
        if operation == 'multiply':
            number = int(input('How many numbers do you want:'))
            x = float(eval('Input number：'))
            if number == 1:
                sum = x
            else:
                sum = x
                while a + 1 < number:
                    y = eval(input('Input number：'))
                    a += 1
                    sum = sum * y

            return sum
        if operation == 'division':
            number = int(input('How many dividends:'))
            x = float(input('Input dividend：'))
            if number == 0:
                sum = x
            else:
                sum = x
                while a < number:
                    y = eval(input('Input divisor：'))
                    a += 1
                    sum = sum / y

            return sum
        if operation == 'square':
            number1 = float(input('Input base number:'))
            number2 = float(input('Input power:'))
            sum = number1 ** number2
            return sum
        if operation == 'remainder':
            number1 = float(input('Input dividend:'))
            number2 = float(input('Input divisor:'))
            sum = number1 % number2
            return sum
    except TypeError:
        print('The type is wrong,please input again')
    except NameError:
        print('The type is wrong,please input again')
    except ValueError:
        print('The type is wrong,please input again')


while True:
    try:
        operation = input('Please enter the calculation method(add/minus/multiply/division/square/remainder) and press ENTER：')
        print('Answer is %f' % function(operation))
    except TypeError:
        print('Please choose among the options')