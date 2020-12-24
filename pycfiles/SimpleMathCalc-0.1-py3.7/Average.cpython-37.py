# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\SimpleMathCalc\Average.py
# Compiled at: 2019-04-02 09:19:22
# Size of source mod 2**32: 654 bytes


def average():
    total = 0
    count = 0
    while True:
        num = input('Input some numbers. When u finished, input "Done" ')
        if num == 'done':
            break
        try:
            num = float(num)
        except:
            print('Please input a number!')
            continue

        total = total + num
        count += 1

    print('The average value of the numbers above is: ', total / count)