# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\Roman.py
# Compiled at: 2001-12-27 15:25:58
__doc__ = '\nLight-weight functions to convert from Roman-Numerals to ints,\nand vice-versa.\n'
factor_list = [
 1000, 500, 100, 50, 10, 5, 1]
roman_equiv = {1000: 'M', 500: 'D', 100: 'C', 50: 'L', 10: 'X', 5: 'V', 1: 'I'}

def IToRoman(num):
    roman = ''
    remainder = num
    factor_index = 0
    for f in factor_list:
        factor_up = f != 1000 and factor_list[(factor_index - 1)] or None
        factor_down = f != 1 and factor_list[(factor_index + 1)] or None
        dividend = remainder / f
        remainder = remainder % f
        if factor_up and dividend == 4:
            roman = roman + roman_equiv[f] + roman_equiv[factor_up]
        elif factor_down and dividend == 1 and remainder / factor_down == 4:
            roman = roman + roman_equiv[factor_down] + roman_equiv[factor_up]
            remainder = remainder % factor_down
        else:
            roman = roman + roman_equiv[f] * dividend
        factor_index = factor_index + 1

    return roman
    return