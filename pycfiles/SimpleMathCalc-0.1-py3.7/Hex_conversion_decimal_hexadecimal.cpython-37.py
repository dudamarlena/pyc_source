# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\SimpleMathCalc\Hex_conversion_decimal_hexadecimal.py
# Compiled at: 2019-04-09 12:35:51
# Size of source mod 2**32: 626 bytes
"""
Spyder Editor

This is a temporary script file.
"""

def dec_hex(str1):
    a = str(hex(eval(str1)))
    b = a.replace('0x', '')
    print('十进制  \t%s\t十六进制\t%s' % (str1, a))
    return b


def hex_dec(str2):
    b = eval('0x' + str2)
    a = str(b).replace('0x', '')
    print('十六进制\t%s\t十进制  \t%s' % (str2, a))
    return b


if __name__ == '__main__':
    str1 = '16'
    str2 = '10'
    print(dec_hex(str1))
    print(hex_dec(str2))