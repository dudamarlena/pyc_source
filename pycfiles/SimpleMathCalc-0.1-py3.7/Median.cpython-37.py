# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\SimpleMathCalc\Median.py
# Compiled at: 2019-04-02 09:36:16
# Size of source mod 2**32: 947 bytes


def median():
    count = dict()
    numbers = list()
    number = input('Input numbers, divide different numbers by a space, when you finished, press "Enter" ')
    numbers = number.split()
    try:
        for num in numbers:
            float(num)

    except:
        print("You have to input numbers! Now let's start again.")
        median()

    length = len(numbers)
    if length % 2 == 1:
        medain_value = numbers[(int((len(numbers) + 1) / 2) - 1)]
        print('The median is ', medain_value)
    if length % 2 == 0:
        num = len(numbers) / 2
        num = int(num)
        medain_value = (float(numbers[(num - 1)]) + float(numbers[num])) / 2
        print('The median is ', medain_value)