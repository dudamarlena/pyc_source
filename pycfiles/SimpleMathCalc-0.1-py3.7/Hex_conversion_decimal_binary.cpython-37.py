# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\SimpleMathCalc\Hex_conversion_decimal_binary.py
# Compiled at: 2019-04-09 12:10:41
# Size of source mod 2**32: 823 bytes


def dtb():
    b = [
     0, 0, 0, 0, 0, 0, 0, 0]
    s = int(input('Please enter a decimal number(less than 255)：'))
    for i in range(0, 8, 1):
        b[i] = int(s % 2)
        s = s // 2

    b.reverse()
    p = [str(i) for i in b]
    print('The binary number is：', ''.join(p), '\n\n\n-----')


def btd():
    a = 0
    d = list(input('Please enter a binary number(less than eight places)：'))
    d.reverse()
    for i in range(0, len(d), 1):
        if int(d[i]) == 1:
            a += pow(2, i)

    print('The decimal number is：', a, '\n\n\n-----')


while True:
    choose = int(input('Decimal to binary please input: 1 \nBinary to decimal please input: 2 \n\ninput: '))
    if choose == 1:
        dtb()
    elif choose == 2:
        btd()
    else:
        break